import logging
import pandas as pd
import yaml

class Normalizer:
    def __init__(self, df):
        self.df = df
        self.config = self.load_config()

    def load_yaml(self, path):
        """
        Load a YAML file.
        :param path:
        :return:
        """
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logging.error(f"Error loading YAML file: {e}")
            return None

    def load_config(self):
        """
        Load schema and data type config.
        """
        return self.load_yaml('config/schema_config.yaml')

    def load_earner_type_dict(self):
        """
        Load the earner type dictionary.
        """
        return self.load_yaml('config/earner_type_dict.yaml')

    def match_earner_type(self, df):
        """
        Match earner type based on the earner type dictionary.
        :return
        """
        fmo_dict = self.load_earner_type_dict().get('earner_type_lookup', {})
        fmo_list = [fmo.lower().strip() for fmo in fmo_dict.get('FMO', [])]

        df.loc[:, 'Earner_Type'] = 'Agent'
        for fmo in fmo_list:
            df.loc[df['Earner_Name'].str.lower().str.strip().str.contains(fmo, na=False), 'Earner_Type'] = 'FMO'

        return df


    def convert_to_datetime(self):
        """
        Align date/time columns to a consistent format.
        """
        for column in self.df.columns:
            if ('date' in column.lower() or 'period' in column.lower()) and self.df[column].dtype in ['object', 'int64', 'float64']:
                try:
                    self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
                    logging.info(f"Column '{column}' successfully converted to datetime.")
                except Exception as e:
                    logging.error(f"Failed to convert column '{column}' to datetime: {e}")
        return self.df

    def align_data_types(self,df):
        """
        Align data types to a consistent format.
        :return:
        """
        fixed_schema_data_types = self.config['fixed_schema_data_types']
        # print("debug----------------", fixed_schema_data_types)
        for column, expected_type in fixed_schema_data_types.items():
            if column in df.columns:
                try:
                    if expected_type == 'datetime':
                        df.loc[:, column] = pd.to_datetime(df[column], errors='coerce')
                    else:
                        df.loc[:, column] = df[column].astype(expected_type)
                        print(f"Column '{column}' successfully converted to {expected_type}.")
                        logging.info(f"Column '{column}' successfully converted to {expected_type}.")
                except Exception as e:
                    logging.warning(f"Failed to align column '{column}' to {expected_type}: {e}")

        return df

    def normalize_dataframe(self, config=None):
        """
        Normalize the dataframe by applying datetime conversion and mappings (if config is provided).
        """
        self.df = self.convert_to_datetime()
        if config:
            self.df, primary_key_mapped = self.apply_config(config)
        else:
            raise ValueError("No configuration provided.")

        if self.df['Earner_Type'].isna().all():
            self.df = self.match_earner_type(self.df)

        self.align_data_types(self.df)
        self.df.drop_duplicates()

        return self.df, primary_key_mapped
    def merge_columns(self, columns, new_column_name):
        """
        Merge multiple columns into a single column.
        :param columns:
        :param new_column_name:
        :return:
        """
        try:
            self.df[new_column_name] = self.df[columns].astype(str).agg(' '.join, axis=1).str.strip()
            logging.info(f"Columns {columns} merged into '{new_column_name}'.")
        except Exception as e:
            logging.error(f"Error merging columns {columns}: {e}")
            raise

        return self.df
        # for column in columns:
        #     if not pd.api.types.is_string_dtype(self.df[column]):
        #         raise TypeError(f"Column '{column}' is not a string. Only string columns can be merged.")
        #
        # self.df[new_column_name] = self.df[columns].astype(str).agg(' '.join, axis=1).str.strip()
        # logging.info(f"Columns {columns} merged into '{new_column_name}'.")
        # return self.df

    def apply_config(self, config):
        fixed_schema = self.config['fixed_schema']
        primary_key = config.get('Primary_Key')

        for fixed_attr in fixed_schema:
            if fixed_attr in config['mappings']:
                mapped_columns = config['mappings'][fixed_attr]
                if isinstance(mapped_columns, list):
                    self.df = self.merge_columns(mapped_columns, fixed_attr)
                    print(f"Merged {mapped_columns} into '{fixed_attr}'.")
                else:
                    if mapped_columns in self.df.columns:
                        self.df.rename(columns={mapped_columns: fixed_attr}, inplace=True)
                        print(f"Mapped '{mapped_columns}' to '{fixed_attr}'.")
                    else:
                        logging.warning(f"Column '{mapped_columns}' not found in the data. Setting '{fixed_attr}' to NaN.")
                        self.df[fixed_attr] = pd.NA


        self.df['Earner_Type'] = pd.NA
        print("Added 'Earner_Type' column with NaN values.")


        # print("before debug----------------", primary_key)
        if not primary_key:
            # print("debug----------------")
            # print(self.df.columns)
            primary_key = [fixed_attr for fixed_attr in fixed_schema if fixed_attr in self.df.columns and fixed_attr != 'Primary_Key']
            # print("after debug----------------", primary_key)
            self.df['Primary_Key'] = self.df[primary_key].astype(str).agg(' '.join, axis=1).str.strip()
            # print(f"Created 'Primary_Key' from {primary_key}.")
        else:
            raise ValueError("No primary key found or mapped.")

        filtered_df = self.df[[col for col in fixed_schema if col in self.df.columns or col == 'Primary_Key']]
        return filtered_df, primary_key


    # delete this function temporarily
    # need to decouple normalizer class and re-add this function
    # def interactive_mapping(self):
    #     """
    #     Allow the user to map columns manually via CLI in the absence of a YAML config.
    #     """
    #     fixed_schema = self.config['fixed_schema']
    #     print("\nNo configuration provided. Enter column mappings for your input data.\n")
    #
    #     mappings = {}
    #     for fixed_attr in fixed_schema:
    #         while True:
    #             print(f"\nPlease select column(s) from your data for '{fixed_attr}' (you can select multiple columns by separating them with commas):")
    #             for idx, column in enumerate(self.df.columns):
    #                 print(f"{idx + 1}. {column}")
    #             selected_columns = input(f"Enter the number(s) corresponding to the column(s) for '{fixed_attr}' (or press Enter to skip): ")
    #             if selected_columns:
    #                 try:
    #                     column_indices = [int(i.strip()) - 1 for i in selected_columns.split(',') if i.strip().isdigit()]
    #                     if all(0 <= idx < len(self.df.columns) for idx in column_indices):
    #                         selected_columns_list = [self.df.columns[i] for i in column_indices]
    #                         if len(selected_columns_list) > 1:
    #                             self.df = self.merge_columns(selected_columns_list, fixed_attr)
    #                             print(f"Merged {selected_columns_list} into '{fixed_attr}'.")
    #                         elif len(selected_columns_list) == 1:
    #                             mappings[selected_columns_list[0]] = fixed_attr
    #                             print(f"Mapped '{selected_columns_list[0]}' to '{fixed_attr}'.")
    #                         break
    #                     else:
    #                         print("Invalid input: Some selected columns are out of range. Please try again.")
    #                 except ValueError:
    #                     print("Invalid input: Please enter valid column numbers.")
    #             else:
    #                 print(f"Skipping mapping for '{fixed_attr}'.")
    #                 self.df[fixed_attr] = pd.NA
    #                 break
    #
    #     self.df.rename(columns=mappings, inplace=True)
    #
    #     filtered_df = self.df[fixed_schema]
    #     return filtered_df











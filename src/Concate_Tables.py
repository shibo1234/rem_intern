import pandas as pd
import json
import os
import re

'''
    This function will read the data from the excel files
'''
def read_and_prepare_data(file_paths, column_mappings):
    dataframes = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path).split('%')[0].strip().lower().replace(' ', '_')
        df = pd.read_excel(file_path)

        if 'Healthfirst' in file_path:
            df['Source'] = 'Healthfirst'
            df['Member Effective Date'] = pd.to_datetime(df['Member Effective Date'], errors='coerce')
            df['Period'] = pd.to_datetime(df['Period'], format='%m/%Y', errors='coerce')

            df.rename(columns=column_mappings['healthfirst_columns'], inplace=True)

        elif 'Emblem' in file_path:
            df['Source'] = 'Emblem'
            df['Effective Date'] = pd.to_datetime(df['Effective Date'], errors='coerce')
            df['Term Date'] = pd.to_datetime(df['Term Date'], errors='coerce')

            if 'Member First Name' in df.columns and 'Member Last Name' in df.columns:
                df['Member_Name'] = df['Member First Name'] + ' ' + df['Member Last Name']
                df.drop(['Member First Name', 'Member Last Name'], axis=1, inplace=True)

            df.rename(columns=column_mappings['emblem_columns'], inplace=True)


        elif 'Centene' in file_path:
            df['Source'] = 'Centene'
            df['Pay Period'] = pd.to_datetime(df['Pay Period'], errors='coerce')
            df['Signed Date'] = pd.to_datetime(df['Signed Date'], errors='coerce')
            df['Effective Date'] = pd.to_datetime(df['Effective Date'], errors='coerce')
            df['Original Effective Date'] = pd.to_datetime(df['Original Effective Date'], errors='coerce')
            df['Member Term Date'] = pd.to_datetime(df['Member Term Date'], errors='coerce')

            df.rename(columns=column_mappings['centene_columns'], inplace=True)

        dataframes.append(df.copy())
        print(f"DataFrame for '{file_name}' has been created and added to the list.")

    return dataframes


'''
    This function will return column mappings
    Column mappings can be customized by user for future tables
    Tables with same meaning of attributes but different names can be mapped to same column to normalize
'''
def load_column_mappings(json_path):
    with open(json_path, 'r') as file:
        column_mappings = json.load(file)
    return column_mappings

'''
    This function will combine all the prepared DataFrames into one.
    It uses an outer join to combine the DataFrames, ignoring index.
'''
def combine_dataframes(dataframes):
    combined_df = pd.concat(dataframes, ignore_index=True, join='outer')
    print(f"Combined DataFrame has {combined_df.shape[0]} rows and {combined_df.shape[1]} columns.")
    combined_df_cleaned = drop_null_columns(combined_df)
    return combined_df_cleaned

'''
    This function prepares and modifies the emblem dataframe.
'''
def prepare_emblem_df(emblem_df):
    emblem_df_copy = emblem_df.copy()
    if 'Member First Name' in emblem_df.columns and 'Member Last Name' in emblem_df.columns:
        emblem_df_copy['Member_Name'] = emblem_df_copy['Member First Name'] + ' ' + emblem_df_copy['Member Last Name']
        emblem_df_copy.drop(['Member First Name', 'Member Last Name'], axis=1, inplace=True)
    return emblem_df_copy

'''
    This function drops columns that contain only null values.
'''
def drop_null_columns(df):
    df_cleaned = df.dropna(axis=1, how='all')
    print(f"Dropped null-only columns. DataFrame now has {df_cleaned.shape[1]} columns.")
    return df_cleaned

'''
    This function extracts key columns from the combined DataFrame.
    This can be customized based on business requirements.
'''
def extract_key_columns(combined_df, key_columns):
    key_df = combined_df[key_columns]
    print(f"Extracted key columns: {key_columns}")
    return key_df


'''
    This function will find duplicate agent names.
'''
def find_duplicate_agents(df):
    duplicate_agents = df[df['Agent_Name'].duplicated(keep=False)]
    duplicate_agents_sorted = duplicate_agents.sort_values(by='Agent_Name')
    return duplicate_agents_sorted


'''
    This function will return top agents by commission for a given year and month.
    The function takes the combined DataFrame, the year, the month, top k candidates as parameters.
'''
def get_top_agents_by_month(combined_df, year, month, k):
    filtered_data = combined_df[
        (combined_df['Commission_Period'].dt.year == year) &
        (combined_df['Commission_Period'].dt.month == month)
        ]

    top_agents = filtered_data.groupby('Agent_Name').agg({
        'Commission_Amount': 'sum',
        'Company': lambda x: ', '.join(x.unique()),
        'Source': lambda x: ', '.join(x.unique())
    }).reset_index()

    top_agents = top_agents.sort_values(by='Commission_Amount', ascending=False).head(k)
def get_top_agents_by_month(combined_df, year, month, k):
    filtered_data = combined_df[
        (combined_df['Commission_Period'].dt.year == year) &
        (combined_df['Commission_Period'].dt.month == month)
        ]

    top_agents = filtered_data.groupby('Agent_Name').agg({
        'Commission_Amount': 'sum',
        'Company': lambda x: ', '.join(x.unique()),
        'Source': lambda x: ', '.join(x.unique())
    }).reset_index()

    top_agents = top_agents.sort_values(by='Commission_Amount', ascending=False).head(k)

    return top_agents
    return top_agents


'''
    This function will write a DataFrame to a CSV file.
    The file will be saved to the specified directory.
'''
def write_to_csv(df, file_name, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, file_name)

    df.to_csv(file_path, index=False)
    print(f"DataFrame has been written to {file_path}")



if __name__ == "__main__":
    json_path = '../config/column_mapping.json'
    column_mappings = load_column_mappings(json_path)
    print(column_mappings)

    file_paths = [
        'Healthfirst%2006.2024%20Commission.xlsx',
        'Emblem%2006.2024%20Commission.xlsx',
        'Centene%2006.2024%20Commission.xlsx'
    ]

    dataframes = read_and_prepare_data(file_paths, column_mappings)

    combined_df = combine_dataframes(dataframes)

    key_columns = ['Commission_Period', 'Commission_Amount', 'Agent_Name', 'Agent_ID', 'Company', 'Plan_Name', 'Source']
    key_df = extract_key_columns(combined_df, key_columns)

    duplicate_agents_sorted = find_duplicate_agents(key_df)

    top_agents_june_2024 = get_top_agents_by_month(key_df, 2024, 6, 10)

    # output_dir = '../csv_output'
    # write_to_csv(combined_df, 'combined_commissions.csv', output_dir)
    # write_to_csv(key_df, 'key_commissions.csv', output_dir)
    # write_to_csv(top_agents_june_2024, 'top_agents_june_2024.csv', output_dir)






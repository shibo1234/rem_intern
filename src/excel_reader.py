import pandas as pd
import os

class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path
        # self.dataframes = self.excel_reader()
        self.file_name = os.path.basename(self.file_path).split('%')[0].strip().lower().replace(' ', '_')
        self.dataframe = self.excel_reader()

    def excel_reader(self):
        """
        Read the excel files and create dataframe
        :return:
        """
        try:
            dataframe = pd.read_excel(self.file_path)
            if not dataframe.empty:
                print(f"DataFrame for '{self.file_name}' has been created.")
                dataframe['Carrier'] = self.file_name
                return dataframe
        except Exception as e:
            print(f"Error while reading the file '{self.file_name}'")
            print(e)
            return None
    def display_dataframe(self):
        """
        Display the dataframes
        :return:
        """
        if self.dataframe is not None:
            print(f"DataFrame from {self.file_path}:")
            print(self.dataframe.columns)
            print(self.dataframe.head())



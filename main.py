import os
import yaml
from src.excel_reader import ExcelReader
from src.normalizer import Normalizer
import argparse
import pandas as pd
from src.command import CommandMeta
import sqlite3

def parse_type(type_str):
    """
    Map types from JSON to Python types.
    """
    if type_str == 'int':
        return int
    elif type_str == 'str':
        return str
    return str

def parse_arguments():
    """
    Parse the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Process commands.')
    subparsers = parser.add_subparsers(
        title="Available commands",
        dest="command",
        help="List of available commands"
    )

    upload_parser = subparsers.add_parser('upload', help='Upload and process Excel files')
    upload_parser.add_argument('file', type=str, help='Path to the Excel file to upload')
    upload_parser.add_argument('--config', type=str, help='Path to the YAML configuration file')

    for cmd in CommandMeta.get_commands().values():
        cmd_parser = subparsers.add_parser(cmd.get_name(), help=cmd.get_help_info())
        if args := cmd.get_args():
            for arg in args:
                cmd_parser.add_argument(f'--{arg["name"]}',
                                        type=parse_type(arg["type"]),
                                        help=cmd.get_help_info())


    parsed_args = parser.parse_args()
    return parsed_args

    # default='yaml/healthfirst_config.yaml',
    # default='yaml/emblem_config.yaml',
    # default='yaml/cenetene_config.yaml',
    # default='data/Healthfirst%2006.2024%20Commission.xlsx',
    # default='data/Emblem%2006.2024%20Commission.xlsx',
    # default='data/Centene%2006.2024%20Commission.xlsx',

def load_config(config_path):
    """
    Load the YAML configuration file if provided.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def validate_primary_key(df, primary_key):
    if not primary_key:
        raise ValueError("No valid Primary Key found or generated.")

    missing_keys = [key for key in primary_key if key not in df.columns]
    if missing_keys:
        raise ValueError(f"Primary Key column(s) not found in the dataframe: {missing_keys}")

    print("Primary Key validation passed.")


def save_to_database(df, file_path='database/normalized.csv', sqlite_db_path='database/normalized.db'):
    if 'Primary_Key' not in df.columns:
        raise ValueError("Merged 'Primary_Key' column not found in the dataframe.")

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        if 'Primary_Key' not in existing_df.columns:
            raise ValueError("Primary_Key not found in existing database.")

        combined_df = pd.concat([existing_df, df]).drop_duplicates(subset='Primary_Key', keep='last')
    else:
        combined_df = df

    combined_df.to_csv(file_path, mode='w', header=True, index=False)
    print(f"Data saved to {file_path}")

    # conn = sqlite3.connect(sqlite_db_path)
    # df.to_sql('normalized_data', conn, if_exists='replace', index=False)
    # print(f"Data saved to {sqlite_db_path} SQLite database")
    #
    # conn.close()

def main():
    args = parse_arguments()
    command_name = args.command

    if command_name == 'upload':
        excel_reader = ExcelReader(args.file)
        excel_reader.display_dataframe()
        df = excel_reader.dataframe
        normalizer = Normalizer(df)
        if args.config:
            config = load_config(args.config)
            if config:
                normalized_df, primary_key = normalizer.normalize_dataframe(config)
                validate_primary_key(normalized_df, primary_key)
                save_to_database(normalized_df)
            else:
                raise ValueError("Error loading config.")
        else:
            raise ValueError("Metadata configuration is required for uploading data.")


    normalized_csv_path = 'database/normalized.csv'

    if not os.path.exists(normalized_csv_path):
        print(f"Error: The normalized CSV at '{normalized_csv_path}' does not exist. Please process an input file first.")
        return

    normalized_dataframe = pd.read_csv(normalized_csv_path)
    command_mapping = {cls.get_name(): cls for cls in CommandMeta.get_commands().values()}
    command_cls = command_mapping.get(command_name)

    if command_cls:
        command_args = vars(args)
        command_parameters = command_cls.get_parameters(command_args)
        command_instance = command_cls()
        command_instance.execute(normalized_dataframe, **command_parameters)
    else:
        print("Command not found. Use --help for available commands.")

if __name__ == "__main__":
    main()


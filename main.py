import os
import yaml
from src.excel_reader import ExcelReader
from src.normalizer import Normalizer
import argparse
import pandas as pd
from src.command import CommandMeta

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
                cmd_parser.add_argument(f'--{arg["name"]}', type=parse_type(arg["type"]), help=cmd.get_help_info())


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

def save_to_database(df, file_path='database/normalized.csv'):
    """
    This is to simulate database by saving csv file
    Write dataframe into existing csv
    :param df:
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, mode='w', header=True, index=False)

    print(f"Data saved to {file_path}")

def main():
    args = parse_arguments()
    command_name = args.command

    if command_name == 'upload':
        excel_reader = ExcelReader(args.file)
        excel_reader.display_dataframe()
        df = excel_reader.dataframe
        normalizer = Normalizer(df)
        # If the user provides METADATA
        if args.config:
            config = load_config(args.config)
            if config:
                normalized_df = normalizer.normalize_dataframe(config)
            else:
                print("Invalid or missing config, switching to interactive mode.")
                normalized_df = normalizer.normalize_dataframe()
        else:
            normalized_df = normalizer.normalize_dataframe()
        save_to_database(normalized_df)

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


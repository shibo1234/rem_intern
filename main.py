import json
import os
import yaml
from src.excel_reader import ExcelReader
from src.normalizer import Normalizer
from src.data_processor import DataProcessor
import argparse
import pandas as pd
from src.command import CommandMeta

def load_json(file_path):
    """
    Load a JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

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

    config_parser = subparsers.add_parser('config', help='Load configuration file')
    config_parser.add_argument('config_file', type=str, help='Path to the YAML configuration file')

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

    normalized_csv_path = 'database/normalized.csv'

    if not os.path.exists(normalized_csv_path):
        print(f"Error: The normalized CSV at '{normalized_csv_path}' does not exist. Please process an input file first.")
        return

    normalized_dataframe = pd.read_csv(normalized_csv_path)
    command_mapping = {cls.get_name(): cls for cls in CommandMeta.get_commands().values()}
    command_cls = command_mapping.get(command_name)

    if command_cls:
        if command_cls.get_args():
            command_args = {arg["name"]: getattr(args, arg["name"]) for arg in command_cls.get_args()}
            command_instance = command_cls(**command_args)
        else:
            command_instance = command_cls()

        command_instance.execute(normalized_dataframe)
    else:
        print("Command not found. Use --help for available commands.")

    # -----------------------------------
    # command_registry = register_commands()
    # args = parse_arguments()
    # if args.upload:
    #     excel_reader = ExcelReader(args.upload)
    #     excel_reader.display_dataframe()
    #     df = excel_reader.dataframe
    #     normalizer = Normalizer(df)
    #     # If the user provides METADATA
    #     if args.config:
    #         config = load_config(args.config)
    #         if config:
    #             normalized_df = normalizer.normalize_dataframe(config)
    #         else:
    #             print("Invalid or missing config, switching to interactive mode.")
    #             normalized_df = normalizer.normalize_dataframe()
    #     else:
    #         normalized_df = normalizer.normalize_dataframe()
    #     save_to_database(normalized_df)
    # # else:
    # #     print("Error: No input file provided. Please specify an input file using --input.")
    #
    #
    # normalized_csv_path = 'database/normalized.csv'
    #
    # if not os.path.exists(normalized_csv_path):
    #     print(f"Error: The normalized CSV at '{normalized_csv_path}' does not exist. Please process an input file first.")
    #     return
    #
    # normalized_dataframe = pd.read_csv(normalized_csv_path)
    # for command_cls in CommandMeta.get_commands().values():
    #     if getattr(args, command_cls.get_name()):
    #
    #         if command_cls.get_args():
    #             command_args = getattr(args, command_cls.get_name())
    #             command_instance = command_cls(*command_args)
    #             command_instance.execute(normalized_dataframe)
    #             # command_args = []
    #             # for subcommand in command_info['subcommand_name']:
    #             #     subcommand_value = getattr(args, subcommand['name'])
    #             #     if subcommand_value:
    #             #         command_args.append(subcommand_value)
    #             # command_instance.execute(*command_args)
    #         else:
    #             command_cls().execute(normalized_dataframe)
    #             break
    #
    # else:
    #     print("No command provided. Use --help for more information.")


if __name__ == "__main__":
    main()


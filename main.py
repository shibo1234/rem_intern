import json
import os
import yaml
from src.excel_reader import ExcelReader
from src.normalizer import Normalizer
from src.data_processor import DataProcessor
import argparse
import pandas as pd

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
    Map string types from JSON to actual Python types.
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
    parser = argparse.ArgumentParser(description='Read and process Excel Files.')

    parser.add_argument(
        '--input',
        type=str,
        # default='data/Healthfirst%2006.2024%20Commission.xlsx',
        # default='data/Emblem%2006.2024%20Commission.xlsx',
        # default='data/Centene%2006.2024%20Commission.xlsx',
        help='Paths to the Excel files to be imported'
    )

    parser.add_argument(
        '--config',
        type=str,
        # default='yaml/healthfirst_config.yaml',
        # default='yaml/emblem_config.yaml',
        # default='yaml/cenetene_config.yaml',
        help='Path to the YAML configuration filee'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    commands = load_json('config/cli_commands.json')

    if not commands:
        print("Error: Failed to load commands from the JSON file.")

    for command, details in commands.items():
        cmd_parser = subparsers.add_parser(command, help=details['help'])
        for arg in details.get('args', []):
            cmd_parser.add_argument(
                arg['name'],
                type=parse_type(arg['type']),
                required=arg['required'],
                help=arg['help']
            )

    return parser.parse_args()

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
    if args.command in ['list_carriers', 'top_k_earners', 'top_k_carriers', 'top_k_plans', 'sql_query']:
        normalized_csv_path = 'database/normalized.csv'

        if not os.path.exists(normalized_csv_path):
            print(f"Error: The normalized CSV at '{normalized_csv_path}' does not exist. Please process an input file first.")
            return

        df = pd.read_csv(normalized_csv_path)
        data_processor = DataProcessor(df)

        if args.command == 'list_carriers':
            data_processor.list_all_carriers()

        elif args.command == 'top_k_earners':
            result = data_processor.find_top_k_earners_over_all_carriers(args.k, args.period)
            print(f"Top {args.k} earners for {args.period}:")
            print(result)

        elif args.command == 'top_k_carriers':
            result = data_processor.find_top_k_carriers(args.k)
            print(f"Top {args.k} carriers:")
            print(result)

        elif args.command == 'top_k_plans':
            result = data_processor.find_top_k_plans(args.k)
            print(f"Top {args.k} plans:")
            print(result)

        elif args.command == 'sql_query':
            result = data_processor.execute_query(args.query)
            print(f"Query result:")
            print(result)

        return

    if args.input:
        excel_reader = ExcelReader(args.input)
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
    else:
        print("Error: No input file provided. Please specify an input file using --input.")

if __name__ == "__main__":
    main()


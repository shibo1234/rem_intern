import os
import yaml
from src.excel_reader import ExcelReader
from src.normalizer import Normalizer
from src.data_processor import DataProcessor
import argparse
import pandas as pd

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
    commands = {
        'list_carriers': {
            'help': 'List all carriers',
        },
        'top_k_earners': {
            'help': 'Find top k earners',
            'args': [
                {'name': '--k', 'type': int, 'required': True, 'help': 'Number of top earners to retrieve'},
                {'name': '--period', 'type': str, 'required': True, 'help': 'Commission period in YYYY-MM format'}
            ]
        },
        'top_k_carriers': {
            'help': 'Find top k carriers',
            'args': [
                {'name': '--k', 'type': int, 'required': True, 'help': 'Number of top carriers to retrieve'}
            ]
        },
        'top_k_plans': {
            'help': 'Find top k plans',
            'args': [
                {'name': '--k', 'type': int, 'required': True, 'help': 'Number of top plans to retrieve'}
            ]
        }
    }

    for command, details in commands.items():
        cmd_parser = subparsers.add_parser(command, help=details['help'])
        for arg in details.get('args', []):
            cmd_parser.add_argument(
                arg['name'],
                type=arg['type'],
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
    if args.command in ['list_carriers', 'top_k_earners', 'top_k_carriers', 'top_k_plans']:
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

    # name = excel_reader.file_name
    # Save the normalized DataFrame to a CSV file into csv_output folder
    # normalized_df.to_csv(f'csv_output/{name}_normalized.csv', index=False)
    # Save the normalized DataFrame to a CSV file into database folder


if __name__ == "__main__":
    main()


import os
import toml
import argparse
from typing import List, Dict


def parse_input() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Search and process TOML configuration files')
    parser.add_argument('--find_all', default='src', 
                       help='Search for and run all config files in the main program folder')
    parser.add_argument('-f', '--folder', default='src', 
                       help='Folder where config files are located')
    parser.add_argument('-c', '--config_file', default='input.toml', 
                       help='Name of the config file')
    return parser.parse_args()


def find_toml_files(directory: str) -> List[str]:
    toml_files = []
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.toml'):
                    toml_files.append(entry.name)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    return toml_files


def read_config_file(name: str) -> Dict:
    try:
        with open(name, 'r') as file:
            conf = toml.load(file)
            return conf.get('config', {})
    except (OSError, toml.TomlDecodeError) as e:
        print(f"Error reading config file {name}: {e}")
        return {}


def get_search_directory(args: argparse.Namespace) -> str:
    return args.folder if args.folder != 'src' else "./"


def main():
    args = parse_input()
    search_dir = get_search_directory(args)
    
    if args.find_all:
        toml_files = find_toml_files(search_dir)
        for file in toml_files:
            file_path = os.path.join(search_dir, file)
            print(f"Reading {file}:")
            config = read_config_file(file_path)
            print(config)
    else:
        config_path = os.path.join(search_dir, args.config_file)
        config = read_config_file(config_path)
        print(config)


if __name__ == "__main__":
    main()
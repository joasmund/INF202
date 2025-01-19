import os
import toml
import argparse

def parseInput():
    parser = argparse.ArgumentParser(description='The code will use default values if no arguments are given.')
    parser.add_argument('--find_all', default='src', help='Search for and run all config files in the main program folder with --find_all')
    parser.add_argument('-f', '--folder', default='src', help='Put in name of the folder where the config files are located.')
    parser.add_argument('-c', '--config_file', default='input.toml', help='Put in name of the config file.')
    args = parser.parse_args()
    return args

def directory_search(directory):
    directories = []
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_dir():
                    directories.append(entry.name)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    return directories

def file_search(directory):
    files = []
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    files.append(entry.name)
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    return files

def get_search_directory(args):
    if args.folder != 'src':  # Check if a custom folder was provided
        return args.folder
    return "./"  # Default to root directory

def create_subfolder_from_file(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    subfolder_path = os.path.join(os.getcwd(), "results", file_name)
    try:
        os.makedirs(subfolder_path, exist_ok=True)
        print(f"Created folder: {subfolder_path}")
    except OSError as e:
        print(f"Error creating subfolder: {e}")

def main():
    args = parseInput()
    search_dir = get_search_directory(args)
    files = file_search(search_dir)
    toml_files = [file for file in files if file.endswith(".toml")]
    print(toml_files)

    for file in toml_files:
        data = toml.load(file)
        print(data)
        create_subfolder_from_file(file)

if __name__ == "__main__":
    main()
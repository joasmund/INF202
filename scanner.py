import os
import toml
import argparse


def parseInput():
    parser = argparse.ArgumentParser(description='The code will use default values if no arguments are given.  ')
    parser.add_argument('--find_all', default='src', help='Search for and run all config files in the main program folder with --find_all')
    parser.add_argument('-f', '--folder', default='src', help='Put in name of the folder where the config files are located. ')
    parser.add_argument('-c', '--config_file', default='input.toml', help='Put in name of the config file. ')
    args = parser.parse_args()
    return args


parseInput()


files = []
directories = []


def directory_search(directory):
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir():
                #print(entry.name)
                directories.append(entry.name)


def file_search(directory):
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                #print(entry.name)
                files.append(entry.name)


directory_search("./")
file_search("./")


toml_files = [file for file in files if file.endswith(".toml")]
print(toml_files)

for file in toml_files:
        data = toml.load(file)
        print(data)


def readConfigFile():
    with open(name, 'r') as file:
        conf = toml.load(file)
    return conf.get('config')

# Run through all .toml files in the folder




""" directory_search("./")
file_search("./") """



""" for root, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".toml"):
            files.append(file)
print(files) """
def get_search_directory():
    args = parseInput()
    if args.folder != 'src':  # Check if a custom folder was provided
        return args.folder
    return "./"  # Default to root directory

search_dir = get_search_directory()
files = []
directory_search(search_dir)
file_search(search_dir)
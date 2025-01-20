import toml
import os
import argparse


def parseInput():
    parser = argparse.ArgumentParser(description='Input config file folder with -f or --find_all')
    parser.add_argument('-f', '--find_all', default='input.toml', help='Put in name of config file. ')
    parser.add_argument('--find_all', default='src', help='Search for and run all config files in the main program folder with --find_all')
    parser.add_argument('-f', '--folder', default='src', help='Put in name of the folder where the config files are located. ')
    parser.add_argument('-c', '--config_file', default='input.toml', help='Put in name of the config file. ')
    args = parser.parse_args()
    return args.file


def readConfigFile(name):
    with open(name, 'r') as file:
        conf = toml.load(file)
    return conf.get('config')


def folder_input():
    folder = argparse.ArgumentParser(description='Input comfig file folder name with -f or --folder')
    folder.add_argument('-f, --folder', default='src', help='Put in name of the folder where the config files are located. ')
    args = folder.parse_args()
    return args.folder


def find_all():
    all = argparse.ArgumentParser(description='Search for and run all config files in the main program folder with --find_all')
    all.add_argument('--find_all', default='src', help='Search for and run all config files in the main program folder with --find_all')
    args = all.parse_args()
    return args.find_all


""" if __name__ == '__main__':
    name = parseInput()
    config = readConfigFile(name)
    print(config) """


with open("input.toml", "r") as f:
    data = toml.load(f)

tStart = 0
print(data)


#readConfigFile(name)


def is_valid_toml_file(file_path):
    """
    Check if a file has a .toml extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file has a .toml extension, False otherwise.
    """
    return os.path.isfile(file_path) and file_path.lower().endswith('.toml')


file_path = "config.toml"

if is_valid_toml_file(file_path):
    print(f"{file_path} is a valid .toml file.")
    # Proceed to read the file
    with open(file_path, "r") as file:
        content = file.read()
        print(content)
else:
    print(f"{file_path} is not a valid .toml file.")

def check_file_type(readConfigFile):
    if isinstance(readConfigFile, str) and readConfigFile.endswith(".toml"):
        print("File type is TOML")
    else:
        raise ValueError("Invalid file type")


def check_starttime(data):
    if "tStart" not in data["settings"]:
        tStart = 0
        return tStart
    elif data["settings"]["tStart"] < 0:
        raise ValueError("Start time must be positive")
    else:       
        pass


def check_endtime(data):
    if data["settings"]["tEnd"] < 0:
        raise ValueError("End time must be positive")
    elif data["settings"]["tEnd"] <= data["settings"]["tStart"]:
        raise ValueError("End time must be greater than start time")
    else:
        pass


def check_steps(data):
    if "nSteps" not in data["settings"]:
        raise ValueError("Number of steps not given")
    elif data["settings"]["nSteps"] <= 0:
        raise ValueError("Number of steps must be positive")
    elif data["settings"]["nSteps"] % 1 != 0:
        raise ValueError("Number of steps must be an integer")
    else:
        pass


def check_for_video(data):
    if "writeFrequency" not in data["IO"]:
        print("writeFrequency not given, no video will be created")
    elif data["IO"]["writeFrequency"] <= 0:
        raise ValueError("writeFrequency must be positive")
    elif data["IO"]["writeFrequency"] % 1 != 0:
        raise ValueError("writeFrequency must be an integer")
    else:
        pass


def check_for_mesh(data):
    if "meshName" not in data["geometry"]:
        raise ValueError("Mesh name not given")
    else:
        pass


def check_for_startposition(data):
    if "xStar" not in data["geometry"]:
        raise ValueError("Start position not given")
    else:
        pass


def check_for_restart_file(data):
    if "restartFile" not in data["IO"] and "tStart" in data["settings"]:
        raise ValueError("Restart file not given. Restart file must be provided if start time is provided")
    else:
        pass


# Denne er vel egentlig ikke nødvendig?
def check_for_restart_params():
    if "restartFile" in data["settings"] and "tStart" not in data["settings"]:
        raise ValueError("Restart file given, but no start time. ")
    else:
        pass


""" # Extract parameters from the config file
starttime = data["settings"]["tStart"]
if starttime < 0:
    raise ValueError("Start time must be positive")
print(starttime)
endtime = data["settings"]["tEnd"]
print(endtime)
steps = data["settings"]["nSteps"]
print(steps)

# Get the start position from the configuration
startposition = data["geometry"]["xStar"]
print(startposition)
meshName = data["geometry"]["meshName"]
print(meshName) """

if __name__ == "__main__":
    #check_file_type(name)
    check_starttime(data)
    check_endtime(data)
    check_steps(data)
    check_for_video(data)
    check_for_mesh(data)
    check_for_startposition(data)
    check_for_restart_file(data)
    print("All checks passed")
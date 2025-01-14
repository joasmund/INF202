import toml


with open("config.toml", "r") as f:
    data = toml.load(f)

print(data)

from parser import readConfigFile, parseInput

config = parseInput()

readConfigFile()

def check_file_type(readConfigFile):
    if isinstance(readConfigFile, str) and readConfigFile.endswith(".toml"):
        print("File type is TOML")
    else:
        raise ValueError("Invalid file type")


def check_starttime(data):
    if data["settings"]["tStart"] < 0:
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
    if "writeFrequency" not in data["settings"]:
        print("writeFrequency not given, no video will be created")
    elif data["settings"]["writeFrequency"] <= 0:
        raise ValueError("writeFrequency must be positive")
    elif data["settings"]["writeFrequency"] % 1 != 0:
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
    if "restartFile" not in data["settings"] and "tStart" in data["settings"]:
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
    check_file_type(data)
    check_starttime(data)
    check_endtime(data)
    check_steps(data)
    check_for_video(data)
    check_for_mesh(data)
    check_for_startposition(data)
    check_for_restart_file(data)
    print("All checks passed")
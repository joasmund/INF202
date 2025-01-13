import toml


import meshio
import numpy as np
import math


with open ("config.toml" , "r") as f:
    data = toml.load(f)

print(data)



up = 0
u_i = 1              #Solution of triangle i at the time t(n) 
u_ngh = 1             #Solution of neighbor triangle ngh at the time t(n)

# Check if the config file is a toml file
def check_file_type(data):
    if not f.endswith(".toml"):
        raise ValueError("Config file must be a toml file")
    else:
        pass


def check_toml(data):
    if not "config" in data:
        raise ValueError("Config file must be a toml file")
    else:
        pass


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
        raise ValueError("writeFrequency not given, no video will be created")
    elif data["settings"]["writeFrequency"] <= 0:
        raise ValueError("writeFrequency must be positive")
    elif data["settings"]["writeFrequency"] % 1 != 0:
        raise ValueError("writeFrequency must be an integer")
    else:
        pass



#extract parameters from the config file
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
print(meshName)



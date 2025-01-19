import os
import toml
import argparse

def parseInput():
    parser = argparse.ArgumentParser(
        description=" input config file name with -f or --file"
    )
    parser.add_argument(
        "-c", "--config", default="input.toml", type=str, help="input config file name"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="folder including the config file"
    )
    parser.add_argument("--find-all", action="store_true", help="find all toml files")
    args = parser.parse_args()
    return args

def readConfig(name):
    if not os.path.exists(name):
        raise FileNotFoundError(f"The config file {name} does not exist.")

    with open(name, "r") as file:
        config = toml.load(file)

    geometry = config["geometry"]
    fish_area = geometry.get("fish_area")
    start_point = geometry.get("initial_oil_area")
    filepath = geometry.get("filepath")

    settings = config["settings"]
    steps = settings.get("nSteps")
    t_start = settings.get("t_start")
    t_end = settings.get("t_end")

    IO = config["IO"]
    writeFrequency = IO.get("writeFrequency")
    restartFile = IO.get("restartFile")
    logName = IO.get("logName")

    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"The mesh file {filepath} does not exist.")

    if not fish_area:
        raise ValueError("Missing fish_area in geometry section.")

    if not start_point:
        raise ValueError("Missing initial_oil_area in geometry section.")

    if not steps or steps <= 0:
        raise ValueError("Missing nSteps in settings section.")

    if restartFile and t_start is None:
        raise ValueError("if restarFile given, must give t_start.")

    if t_end is None or t_end <= t_start:
        raise ValueError("Missing t_end in or t_end <= t_start in settings section.")

    if not writeFrequency:
        writeFrequency = -1000

    if not restartFile:
        t_start = 0

    if not logName:
        logName = "logfile.log"

    print(f"Successfully read config file {name}")
    return config

def process_all_configs(folder):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"The folder {folder} does not exist.")

    toml_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".toml")]
    if not toml_files:
        print("No .toml files found in the specified folder.")
        return []

    return toml_files

def main():
    args = parseInput()

    if args.find_all:
        if args.file:
            toml_files = process_all_configs(args.file)
            for toml_file in toml_files:
                print(f"Processing: {toml_file}")
                try:
                    config = readConfig(toml_file)
                    print(config)
                except Exception as e:
                    print(f"Error reading {toml_file}: {e}")
        else:
            print("Please provide a folder with -f to find all .toml files.")
    elif args.config:
        try:
            config = readConfig(args.config)
            print(config)
        except Exception as e:
            print(f"Error reading {args.config}: {e}")
    else:
        print("Please provide either --find-all with a folder (-f) or a specific config file with -c.")

if __name__ == "__main__":
    main()

import argparse
import toml



def parseInput():
    parser = argparse.ArgumentParser(description=' Input comfig file name with -f or --file')
    parser.add_argument ('-f', '--file', default = 'config.toml', help='Put in name of config file. ', required=True)
    args = parser.parse_args()
    return args.file

def readConfigFile(name):
    with open (name, 'r') as file:
        conf = toml.load(file)
    return conf.get('config')

if __name__ == '__main__':
    name = parseInput()
    config = readConfigFile(name)
    print(config)

def folder_input():
    folder = argparse.ArgumentParser(description=' Input comfig file name with -f or --file')
    folder.add_argument 


""" def video_writer():
    videoArg = argparse.ArgumentParser(description=' To create a video of the simulation, make sure to have writeFrequency in the config file')
    videoArg.add_
 """
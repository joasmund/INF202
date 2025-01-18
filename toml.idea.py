import argparse
"""

kun ment som et forslag

"""

def parseInput():
    parser = argparse.ArgumentParser(description="Kjør validering av en eller flere TOML-filer")
    parser.add_argument("-f", "--folder", default="src", help="Navn på filen der toml. ligger")
    parser.add_argument("-c", "--config_file", default="input.toml", help="Navn på enkeltfil (.toml)")
    parser.add_argument("--find_all", action="store_true", help="Hvis satt, sjekk alle toml.filer i mappe")

    args = parser.parse_args()
    return args
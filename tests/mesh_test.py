import pytest
import os

file = "bay.msh"



def test_file_type():
    if file.endswith(".msh"):
        print("Correct file type!")
    else:
        print("Incorrect file type.")

def test_file_exists():
    if os.path.exists(file):
        print("File exists!")
    else:
        print("File does not exist.")

def test_file_size():
    if os.path.getsize(file) > 0:
        print("File has size!")
    else:
        print("File is empty.")
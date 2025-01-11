import pytest
import sys
import os

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from structure_start import Cell, Line, Triangle




def test_positive_length(input_n, expected):
    print(f"{input_n}")
    assert Cell.cell_size() == expected

class TestPositiveLength:
    def test_positive_length(self):
        c = Cell([1, 2], 1)
        assert c.cell_size() == 1


def test_line():
    l = Line([1, 2], 1)
    assert l.__str__() == "Line with id 1: []"

def test_midpoint():
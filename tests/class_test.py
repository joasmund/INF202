import pytest
import sys
import os


# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))


from structure_start import *




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
    l = Cell([1, 2], 1)
    assert l.midpoint() == 1.5

def test_computeNeighbors():
    l = Line([1, 2], 1)
    l.computeNeighbors([Line([2, 3], 2)])
    assert l._neighbors == [2]

def test_vertex():
    v = Vertex([1], 1)
    assert v.__str__() == "Vertex with id 1: []"



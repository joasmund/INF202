import pytest
from alfa import *

def test_cell_type():
    line = Line(1, [1, 2])
    assert isinstance(line, Cell) == 

def test_cell_size_positive():
    c = Line(0, [1, 2])
    assert c.cell_size() == 1


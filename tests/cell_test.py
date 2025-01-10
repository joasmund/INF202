from ..structure_start import Cell, Line, Triangle
import pytest

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

test_line()

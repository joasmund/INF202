import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import alfa
#Need to have BoundaryPoint and Point classes defined in alfa.py

@pytest.fixture
def cells():
    #Create and return a list of cells to be used in tests 
    points_values = np.linspace(0, 1, 10)
    cells = []

    for idx, (pt1, pt2) in enumerate(zip(points_values[:-1], points_values[1:])):
        cells.append(Line(idx, [pt1, pt2]))
    cells.append(BoundaryPoint(0, points_values[0]))
    cells.append(BoundaryPoint(len(cells), points_values[-1]))

@pytest.mark.parametrize("cell_index", range(9)) #Indices for all line cells
def test_line_cell_size_positive(cells, cell_index):
    cell = cells[cell_index]
    assert cell.cell_size() > 0, f"Line cell {cell.id} has non-positive size"

@pytest.mark.parametrize("cell_index", range(9)) #Indices for boundary_point cells
def test_boundary_point_cell_size_zero(cells, cell_index):
    cell = cells[cell_index]
    assert cell.cell_size() == pytest.approx(0), f"BoundaryPoint cell {cell.id} has non-zero size"


""" def test_cell_type():
    line = Line(1, [1, 2])
    assert isinstance(line, Cell) ==  """

def test_cell_size_positive():
    c = Line(0, [1, 2])
    assert c.cell_size() == 1

def test_psitive_ids(cells):
    for cell in cells:
        assert cell.id >= 0, f"Cell {cell.id} is not positive"

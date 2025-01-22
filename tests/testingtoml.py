"""
Test for toml

"""

import pytest
import toml
import os

def validate_toml_file(file_path):
    if not os.path.isfile(file_path) or not file_path.endswith('.toml'):
        raise ValueError(f"{file_path} is not a valid TOML file.")

    with open(file_path, "r") as file:
        data = toml.load(file)

    # Essential checks
    if data["settings"]["tStart"] < 0:
        raise ValueError("Start time (tStart) must be positive.")
    if data["settings"]["tEnd"] <= data["settings"]["tStart"]:
        raise ValueError("End time (tEnd) must be greater than start time (tStart).")
    if data["settings"]["nSteps"] <= 0:
        raise ValueError("Number of steps (nSteps) must be positive.")
    if "meshName" not in data["geometry"] or not data["geometry"].get("meshName"):
        raise ValueError("Mesh name is missing or empty in geometry.")
    if "xStar" not in data["geometry"] or not data["geometry"].get("xStar"):
        raise ValueError("Start position (xStar) is missing or empty in geometry.")

    # Optional field checks
    if "restartFile" in data.get("IO", {}) and data["settings"]["tStart"] > 0:
        if not data["IO"].get("restartFile"):
            raise ValueError("Restart file must be provided if start time (tStart) is greater than 0.")

    return "All validations passed!"

# Pytest test cases
def test_valid_toml_file(tmp_path):
    valid_toml_content = """
    [settings]
    tStart = 0.1
    tEnd = 0.2
    nSteps = 500

    [geometry]
    meshName2 = "bay.msh"
    meshName = "simple.msh"
    borders = [[0.0, 0.45], [0.0, 0.2]]
    xStar = [0.35, 0.45]

    [IO]
    logName = "log"
    writeFrequency = 10
    restartFile = "input/solution.txt"
    """
    file_path = tmp_path / "valid_input.toml"
    file_path.write_text(valid_toml_content)

    assert validate_toml_file(str(file_path)) == "All validations passed!"

def test_invalid_tStart(tmp_path):
    invalid_toml_content = """
    [settings]
    tStart = -1
    tEnd = 0.2
    nSteps = 500

    [geometry]
    meshName2 = "bay.msh"
    meshName = "simple.msh"
    borders = [[0.0, 0.45], [0.0, 0.2]]
    xStar = [0.35, 0.45]

    [IO]
    logName = "log"
    writeFrequency = 10
    restartFile = "input/solution.txt"
    """
    file_path = tmp_path / "invalid_tStart.toml"
    file_path.write_text(invalid_toml_content)

    with pytest.raises(ValueError, match="Start time \(tStart\) must be positive."):
        validate_toml_file(str(file_path))

def test_invalid_tEnd(tmp_path):
    invalid_toml_content = """
    [settings]
    tStart = 0.2
    tEnd = 0.1
    nSteps = 500

    [geometry]
    meshName2 = "bay.msh"
    meshName = "simple.msh"
    borders = [[0.0, 0.45], [0.0, 0.2]]
    xStar = [0.35, 0.45]

    [IO]
    logName = "log"
    writeFrequency = 10
    restartFile = "input/solution.txt"
    """
    file_path = tmp_path / "invalid_tEnd.toml"
    file_path.write_text(invalid_toml_content)

    with pytest.raises(ValueError, match="End time \(tEnd\) must be greater than start time \(tStart\)."):
        validate_toml_file(str(file_path))

def test_missing_meshName(tmp_path):
    invalid_toml_content = """
    [settings]
    tStart = 0.1
    tEnd = 0.2
    nSteps = 500

    [geometry]
    meshName2 = "bay.msh"
    borders = [[0.0, 0.45], [0.0, 0.2]]
    xStar = [0.35, 0.45]

    [IO]
    logName = "log"
    writeFrequency = 10
    restartFile = "input/solution.txt"
    """
    file_path = tmp_path / "missing_meshName.toml"
    file_path.write_text(invalid_toml_content)

    with pytest.raises(ValueError, match="Mesh name is missing or empty in geometry."):
        validate_toml_file(str(file_path))

def test_missing_xStar(tmp_path):
    invalid_toml_content = """
    [settings]
    tStart = 0.1
    tEnd = 0.2
    nSteps = 500

    [geometry]
    meshName = "simple.msh"
    borders = [[0.0, 0.45], [0.0, 0.2]]

    [IO]
    logName = "log"
    writeFrequency = 10
    restartFile = "input/solution.txt"
    """
    file_path = tmp_path / "missing_xStar.toml"
    file_path.write_text(invalid_toml_content)

    with pytest.raises(ValueError, match="Start position \(xStar\) is missing or empty in geometry."):
        validate_toml_file(str(file_path))

def test_restartFile_required(tmp_path):
    invalid_toml_content = """
    [settings]
    tStart = 0.1
    tEnd = 0.2
    nSteps = 500

    [geometry]
    meshName = "simple.msh"
    borders = [[0.0, 0.45], [0.0, 0.2]]
    xStar = [0.35, 0.45]

    [IO]
    logName = "log"
    writeFrequency = 10
    """
    file_path = tmp_path / "missing_restartFile.toml"
    file_path.write_text(invalid_toml_content)

    with pytest.raises(ValueError, match="Restart file must be provided if start time \(tStart\) is greater than 0."):
        validate_toml_file(str(file_path))

def test_invalid_file_path():
    with pytest.raises(ValueError, match="not_a_file.toml is not a valid TOML file."):
        validate_toml_file("not_a_file.toml")

"""

making a def so we can be sure on the input

""""

def test_real_input_toml():
    file_path = os.path.join("configExamples", "input.toml")
    try:
        assert validate_toml_file(file_path) == "All validations passed!"
    except ValueError as e:
        pytest.fail(f"Validation failed: {e}")
"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest
import importlib
task = importlib.import_module('.task_read_write', 'practice.2_python_part_2')

def test_read_write(tmpdir):
    numbers = [54,577,84,5,14,51,23,22,1]
    str_numbers = [str(number) for number in numbers]
    out = ", ".join(str_numbers)

    dir = tmpdir.mkdir("files_temp") # temporary folder

    # files with content
    for i, number in enumerate(str_numbers):
        file = dir.join(f"file_{i+1}.txt")
        file.write(number)
        
    file = tmpdir.join('result_temp.txt') # temporary result file

    line = task.read_write_values(dir, file.strpath) # task call

    assert line == out
    assert file.read() == out
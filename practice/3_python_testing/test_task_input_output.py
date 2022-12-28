"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""

# https://andressa.dev/2019-07-20-using-pach-to-test-inputs/

from unittest.mock import patch
import importlib
task = importlib.import_module('.task_input_output', 'practice.2_python_part_2')

# found 2 ways

def test_read_numbers_without_text_input():
    with patch('builtins.input', return_value='1, 2, 3, 4, 5'):
        res = task.read_numbers(5)
        assert res == 'Avg: 3.00'


@patch('builtins.input', return_value='1, 2, Text')
def test_read_numbers_with_text_input(mock_input):
    res = task.read_numbers(3)
    assert res == 'Avg: 1.50'

@patch('builtins.input', return_value='hello, world, foo, bar, baz')
def test_read_only_text(mock_input):
    res = task.read_numbers(5)
    assert res == 'No numbers entered'
from src import task_2
import pytest

def test_log():
    assert task_2.math_calculate('log', 1024, 2) == 10.0

def test_ceil():
    assert task_2.math_calculate('ceil', 10.7) == 11

def test_not_found():
    with pytest.raises(task_2.OperationNotFoundException) as e:
        task_2.math_calculate('notafunction', 22)
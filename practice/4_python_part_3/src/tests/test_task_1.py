from src import task_1

# test exception WrongFormatException calculate_days('10-07-2021')
# calculate_days('2021-10-07')
# calculate_days('2021-10-05'
import pytest
from datetime import datetime
from freezegun import freeze_time

@freeze_time("2022-12-16")
def test_correct_format():
    days = task_1.calculate_days("2022-12-01") # 15 days ago
    assert days == 15

@freeze_time("2022-12-16")
def test_negative():
    days = task_1.calculate_days("2023-12-16") # next year
    assert days == -365

@freeze_time("2022-12-16")
def test_incorrect_format():
    with pytest.raises(task_1.WrongFormatException) as e:
        days = task_1.calculate_days("12-01-2022")
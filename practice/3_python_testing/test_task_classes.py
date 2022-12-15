"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
import pytest
import datetime
import importlib
task_classes = importlib.import_module('.task_classes', 'practice.2_python_part_2')

@pytest.fixture
def teacher():
    return task_classes.Teacher('Dmitry', 'Orlyakov')

@pytest.fixture
def student():
    return task_classes.Student('Vladislav', 'Popov')

@pytest.fixture
def expired_homework(teacher):
    return teacher.create_homework('Learn functions', 0)

def test_names(teacher, student):
    assert teacher.last_name == "Dmitry"
    assert student.first_name == "Popov"

def test_expired_homework(expired_homework):
    assert expired_homework.created.date() == datetime.datetime.today().date()
    assert expired_homework.deadline == datetime.timedelta(days=0)
    assert expired_homework.text == "Learn functions"

def test_homework(teacher, student):
    # create function from method and use it
    create_homework_too = teacher.create_homework
    deadline = 5
    oop_homework = create_homework_too('create 2 simple classes', deadline)
    assert student.do_homework(oop_homework) == oop_homework
    assert oop_homework.deadline == datetime.timedelta(days=deadline)

def test_late(capfd, student, expired_homework):
    student.do_homework(expired_homework)
    out, err = capfd.readouterr()
    assert out == "You are late\n"
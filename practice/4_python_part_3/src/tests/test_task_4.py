from src import task_4
from unittest.mock import Mock, patch
import argparse

input_mock = Mock()
input_mock.args.return_value = 'task_4.py 2 --fake-address=address --some_name=name'

@patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(number=4, data=['--fake-address=address','--some_name=name']))
def test_command(mock_args):
    task_4.print_name_address()
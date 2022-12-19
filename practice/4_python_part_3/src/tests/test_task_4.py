from src import task_4
from unittest.mock import Mock, patch

input_mock = Mock()
input_mock.args.return_value = 'task_4.py 2 --fake-address=address --some_name=name'
"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

# !!! https://stackoverflow.com/questions/37367331/is-it-possible-to-use-argparse-to-capture-an-arbitrary-set-of-optional-arguments
# https://www.digitalocean.com/community/tutorials/how-to-use-argparse-to-write-command-line-programs-in-python
# https://learnpython.com/blog/argparse-module/
# https://stackoverflow.com/questions/27181084/how-to-iterate-over-arguments

import argparse
import sys
from faker import Faker

faker = Faker()

def print_name_address(args: argparse.Namespace) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('num', type=int)
    args, unknown = parser.parse_known_args()
    
    # add fields to parser
    for arg in unknown:
        if arg.startswith(("-", "--")):
            parser.add_argument(arg.split('=')[0])
    args = parser.parse_args()

    # remove number from args
    number = args.num
    del args.num

    dict_ls = list()
    for i in range(number):
        new_dict = dict()
        for field, provider in vars(args).items():
            new_dict[field] = eval(f"faker.{provider}()")
        print(new_dict)
        dict_ls.append(new_dict)
    
    return dict_ls
    

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""

print_name_address(sys.argv)
# https://superfastpython.com/multithreaded-file-loading/#Takeaways

import os
from random import randint
import sys
import csv
from pathlib import Path
import multiprocessing

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'
sys.set_int_max_str_digits(500000) # 


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    
    write_file(n, f1)

    return f1

def write_file(file, content):
    with open(f'{OUTPUT_DIR}/{file}.txt', 'w') as f:
        f.write(f'{content}')

def func1(array: list):
    with multiprocessing.Pool() as pool:
        pool.map(fib, array)

def func2(result_file: str, folder: str):
    src_data = os.path.abspath(os.path.join(os.path.dirname( __file__ ), folder))
    open(result_file, 'w').close()
    for file in os.listdir(src_data):
        file_split = file.split('.')
        if file_split[-1] == 'csv': continue
        ordinal = int(file_split[0]) # filename to number
        with open(os.path.join(src_data, file)) as f:
            fibo = f.read()
            with open(result_file, 'a+') as out:
                csv_out = csv.writer(out)
                csv_out.writerow((ordinal, fibo))

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    arr = [randint(1000, 100000) for _ in range(1000)]
    arr2 = [5, 1, 8, 10]

    func1(array=arr2)
    func2(result_file=RESULT_FILE, folder=OUTPUT_DIR)
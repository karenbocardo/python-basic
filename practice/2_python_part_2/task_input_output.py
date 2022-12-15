"""
Write function which reads a number from input nth times.
If an entered value isn't a number, ignore it.
After all inputs are entered, calculate an average entered number.
Return string with following format:
If average exists, return: "Avg: X", where X is avg value which rounded to 2 places after the decimal
If it doesn't exists, return: "No numbers entered"
Examples:
    user enters: 1, 2, hello, 2, world
    >>> read_numbers(5)
    Avg: 1.67
    ------------
    user enters: hello, world, foo, bar, baz
    >>> read_numbers(5)
    No numbers entered

"""
from statistics import mean

def read_numbers(n: int) -> str:
    numbers = list()
    input_line = input() # changing input to one string separated by commas + space
    input_line = input_line.split(', ')
    for i in range(n):
        x = input_line[i]
        if x.isnumeric():
            numbers.append(float(x))
    if numbers:
        avg = mean(numbers)
        return f"Avg: {avg:.2f}"
    else:
        return "No numbers entered"
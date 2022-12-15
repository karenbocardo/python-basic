"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
import os

def read_write_values(folder="./files", res="result.txt"):
    content = list()

    for file in os.listdir(folder):
        with open(os.path.join(folder, file)) as f:
            content.append(f.read())
    
    line = ", ".join(content)
    with open(res, "w") as f:
        f.write(line)
    return line

if __name__ == '__main__':
    read_write_values()
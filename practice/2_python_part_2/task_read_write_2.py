"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""

def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words

def write_words(words, filename, encoding, separator, reverse=False):
    if reverse:
        words.reverse()
    with open(filename, "w", encoding=encoding) as f:
        f.writelines(separator.join(words))

def write_files(words, filenames):
    one, two = filenames
    write_words(words, one, "utf-8", "\n")
    write_words(words, two, "CP1252", ",", True)

if __name__ == '__main__':
    words = generate_words(3)
    filenames = (f"file_{x+1}.txt" for x in range(2))
    write_files(words, filenames)
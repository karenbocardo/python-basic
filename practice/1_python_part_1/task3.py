"""
Write function which receives list of text lines (which is space separated words) and word number.
It should enumerate unique words from each line and then build string from all words of given number.
Restriction: word_number >= 0
Examples:
    >>> build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1)
    'b 2 dog'
    >>> build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
    'a cat'
    >>> build_from_unique_words('1 2', '1 2 3', word_number=10)
    ''
    >>> build_from_unique_words(word_number=10)
    ''
"""
from typing import Iterable

def unique_filter(ls):
    filter = []
    seen = set()
    for elem in ls:
        if not elem in seen:
            filter.append(elem)
            seen.add(elem)
    return filter
def build_from_unique_words(*lines: Iterable[str], word_number: int) -> str:
    words = list()
    for line in lines:
        filtered = unique_filter(line.split())
        if word_number < len(filtered):
            words.append(filtered[word_number])
    out = " ".join(words)
    return out
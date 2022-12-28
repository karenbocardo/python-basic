"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import importlib
task = importlib.import_module('.task_read_write_2', 'practice.2_python_part_2')

def test_words(tmpdir):
    words = task.generate_words()

    one = tmpdir.join("file1.txt")
    two = tmpdir.join("file2.txt")
    
    task.write_files(words, [one, two])

    print(one.read())
    out_one = "\n".join(words)
    out_two = ",".join(reversed(words))

    assert one.read() == out_one
    assert two.read() == out_two
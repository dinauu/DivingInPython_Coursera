import os
import tempfile


class File:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.current = 0

    def write(self, data):
        with open(self.path_to_file, 'w') as file:
            file.write(data)

    def __add__(self, file):
        with open(self.path_to_file) as first_file:
            first_data = first_file.read()
        with open(file.path_to_file) as second_file:
            second_data = second_file.read()
        common_file = File(os.path.join(tempfile.gettempdir(), 'common.txt'))
        common_file.write(first_data + second_data)
        return common_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path_to_file) as file:
            lines = file.readlines()
        if self.current >= len(lines):
            raise StopIteration
        item = lines[self.current]
        self.current += 1
        return item

    def __str__(self):
        return self.path_to_file

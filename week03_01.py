class FileReader():
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def read(self):
        try:
            with open(self.path_to_file) as file:
                return file.read()
        except IOError:
            return ''

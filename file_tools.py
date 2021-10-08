import os


class FileSetInfo:
    """
    class representing size and lines count of the set of files
    """

    def __init__(self, total_size, total_lines, total_files):
        self.total_size = total_size
        self.total_lines = total_lines
        self.total_files = total_files

    def add(self, file_set_info):
        self.total_files += file_set_info.total_files
        self.total_lines += file_set_info.total_lines
        self.total_size += file_set_info.total_size

    @staticmethod
    def empty():
        return FileSetInfo(0, 0, 0)


class FileManager:
    """
    Helper class for file management
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def get_size(self):
        """
        get size of the file in bytes
        """
        return os.path.getsize(self.file_path)

    def get_lines_count(self):
        """
        get number of lines in the file
        """
        with open(self.file_path, 'r') as file:
            return sum(1 for _ in file)

    def has_extension(self, extension):
        """
        check if the file has given file extension (e.g. '.py')

        :param extension: given file extension (e.g. '.py')
        """
        return self.file_path.endswith(f'.{extension}')


def get_path_with_slashes(path):
    """
    get path using forward slashes (e.g. replace back-slash by forward slash on Windows)
    """
    return path.replace('\\', '/')

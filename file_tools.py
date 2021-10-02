import os


class FileSystemNodeInfo:
    """
    class representing size and lines count of the file OR set of files
    """

    def __init__(self, size, lines):
        self.size = size
        self.lines = lines


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


def inspect_directory(directory, file_extension, debug_prints):
    """
    inspect the given directory and count lines & size of all files with the given file extension

    :param directory: the directory to inspect
    :param file_extension: extension of the files that we're looking for
    :param debug_prints: should the program print debug prints? (e.g. 'file XXX processed)
    """
    items = os.listdir(directory)
    files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
    directories = [f for f in items if os.path.isdir(os.path.join(directory, f))]

    (total_size, total_lines) = (0, 0)

    for sub_dir in directories:
        directory_path = os.path.join(directory, sub_dir)
        directory_size = inspect_directory(directory_path, file_extension, debug_prints)
        total_size += directory_size.size
        total_lines += directory_size.lines

    for file in files:
        file_path = os.path.join(directory, file)
        file_manager = FileManager(file_path)
        if not file_manager.has_extension(file_extension):
            continue

        total_size += file_manager.get_size()
        total_lines += file_manager.get_lines_count()

        if debug_prints:
            file_path = file_path.replace('\\', '/')
            print(f'{file_path} processed')

    return FileSystemNodeInfo(total_size, total_lines)

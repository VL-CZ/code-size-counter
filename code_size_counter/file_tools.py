import os

NO_EXTENSION_PLACEHOLDER = "(NONE)"


class FileSetSize:
    """
    class representing
     - total size
     - total lines count
     - number of files

     of a set of files
    """

    def __init__(
        self,
        total_files,
        total_lines,
        total_size,
    ):
        """
        :param total_size: total size of all files in the set (in bytes)
        :param total_lines: total lines of code of all files in the set
        :param total_files: number of files in the set
        """
        self.total_size = total_size
        self.total_lines = total_lines
        self.total_files = total_files

    def add(self, other):
        """
        add FileSetSize to this object

        e.g. sum the corresponding fields

        :param other:
        :return: New fileset size with corresponding fields summed
        """
        return FileSetSize(
            self.total_files + other.total_files,
            self.total_lines + other.total_lines,
            self.total_size + other.total_size,
        )

    def __add__(self, other):
        return self.add(other)

    def __eq__(self, other):
        return (
            self.total_size == other.total_size
            and self.total_lines == other.total_lines
            and self.total_files == other.total_files
        )

    def __repr__(self):
        return f"(Files, Lines, Size): ({self.total_files}, {self.total_lines}, {self.total_size})"

    @staticmethod
    def empty():
        """
        create empty instance of class FileSetSizeInfo

        :return:
        """
        return FileSetSize(0, 0, 0)


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
        with open(self.file_path, "r") as file:
            return sum(1 for _ in file)

    def has_one_of_extensions(self, extensions):
        """
        check if the file has one of the extensions

        :param extensions: collection of expected extensions
        """
        return any(self._has_extension(e) for e in extensions)

    def get_extension(self):
        """
        get file extension
        """
        path_after_dot = self.file_path.split(".")[-1]

        if any(delim in path_after_dot for delim in ["/", "\\"]):
            return NO_EXTENSION_PLACEHOLDER
        else:
            return path_after_dot

    def _has_extension(self, extension):
        """
        check if the file has given file extension (e.g. '.py')

        :param extension: given file extension (e.g. '.py')
        """
        return self.file_path.endswith(f".{extension}")


def get_path_with_slashes(path):
    """
    get path using forward slashes (e.g. replace back-slash by forward slash on Windows)
    """
    return path.replace("\\", "/")

import os

from src.file_tools import FileSetSize, FileManager, get_path_with_slashes


class CodeSizeCounter:
    """
    class responsible for computing the source code size in the given directory
    """

    def __init__(self, directory, file_extensions, print_logs, excluded_items):
        """
        :param directory: the directory where to search files
        :param file_extensions: extensions of the files that we're searching
        :param print_logs: should the program print its progress? (e.g. 'file XXX processed')
        :param excluded_items: absolute path to directories & files to exclude
        """
        self._directory = directory
        self._file_extensions = file_extensions
        self._print_logs = print_logs
        self._excluded_items = excluded_items

        self._check_if_paths_exist()

    def calculate_size(self):
        """
        count lines, size (in bytes) and number of files in the directory with the selected file extension
        """
        return self._calculate_size(self._directory)

    def _calculate_size(self, directory):
        """
        count lines, size (in bytes) and number of files in the directory with the selected file extension

        :param directory: directory where to search files
        """

        # if it's in excluded files/directories, return
        if self._is_excluded(directory):
            return FileSetSize.empty()

        items = os.listdir(directory)
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        directories = [d for d in items if os.path.isdir(os.path.join(directory, d))]

        file_set_size = FileSetSize.empty()

        for sub_dir in directories:  # add the size of all subdirs
            directory_path = os.path.join(directory, sub_dir)
            directory_size = self._calculate_size(directory_path)
            file_set_size.add(directory_size)

        for file in files:  # add the size of all files
            file_path = os.path.join(directory, file)
            file_manager = FileManager(file_path)
            if (not file_manager.has_one_of_extensions(self._file_extensions)) or self._is_excluded(file_path):
                continue

            file_size = FileSetSize(file_manager.get_size(), file_manager.get_lines_count(), 1)
            file_set_size.add(file_size)

            if self._print_logs:
                print(f'{get_path_with_slashes(file_path)} processed')

        return file_set_size

    def _is_excluded(self, path):
        """
        check if the directory/file is excluded from the code size calculation

        :param path: path of the directory/file to check
        """
        return any(os.path.samefile(path, ex) for ex in self._excluded_items)

    def _check_if_paths_exist(self):
        """
        check if paths to the selected directory and excluded items are valid
        """
        all_paths = self._excluded_items + (self._directory,)
        all_paths_exist = all(os.path.exists(path) for path in all_paths)
        if not all_paths_exist:
            invalid_paths = map(
                get_path_with_slashes,
                filter(lambda path: not os.path.exists(path), all_paths)
            )
            raise FileNotFoundError(f'The following paths are not valid {list(invalid_paths)}')

import os

from code_size_counter.file_tools import (
    FileSetSize,
    FileManager,
    get_path_with_slashes,
)


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
        self._include_all_files = file_extensions == ()
        self._print_logs = print_logs
        self._excluded_items = excluded_items
        self._sizes_dict = {}

        self._check_if_paths_exist()

    def calculate_size(self):
        """
        count lines, size (in bytes) and number of files in the directory with the selected file extension

        :return: dictionary, whose keys are file extensions and values are corresponding FileSetSize objects
        """
        self._calculate_size(self._directory)
        return self._sizes_dict

    def _calculate_size(self, directory):
        """
        count lines, size (in bytes) and number of files in the directory with the selected file extension

        :param directory: directory where to search files
        """

        # if it's in excluded files/directories, return
        if self._is_excluded(directory):
            return

        items = os.listdir(directory)
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        directories = [d for d in items if os.path.isdir(os.path.join(directory, d))]

        for sub_dir in directories:  # add the size of all subdirs
            directory_path = os.path.join(directory, sub_dir)
            self._calculate_size(directory_path)

        for file in files:  # add the size of all files
            file_path = os.path.join(directory, file)
            file_manager = FileManager(file_path)
            if (
                not self._include_all_files
                and not file_manager.has_one_of_extensions(self._file_extensions)
            ) or self._is_excluded(file_path):
                continue

            try:
                file_size = FileSetSize(
                    1, file_manager.get_lines_count(), file_manager.get_size()
                )

                ext = file_manager.get_extension()

                # Add to sizes_dict
                self._add_file_size(file_size, ext)

                if self._print_logs:
                    print(f"{get_path_with_slashes(file_path)} processed")
            except (
                UnicodeDecodeError
            ):  # Ignore binary files and other ones that can't be decoded
                if self._print_logs:
                    print(
                        f"Skipping {get_path_with_slashes(file_path)} , which can't be opened in read mode"
                    )

    def _add_file_size(self, file_set_size, file_extension):
        """
        Add file set size to `_sizes_dict` dictionary
        """
        new_size = (
            self._sizes_dict[file_extension] + file_set_size
            if file_extension in self._sizes_dict
            else file_set_size
        )
        self._sizes_dict[file_extension] = new_size

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
                filter(lambda path: not os.path.exists(path), all_paths),
            )
            raise FileNotFoundError(
                f"The following paths are not valid {list(invalid_paths)}"
            )

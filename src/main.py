import os
from argparse import ArgumentParser

from file_tools import FileSetSize, FileManager, get_path_with_slashes


class CodeSizeCounter:
    """
    class responsible for computing the source code size in the given directory
    """

    def __init__(self, directory, file_extensions, print_logs, excluded_items):
        """
        :param directory: the directory where to search files
        :param file_extensions: extension of the files that we're searching
        :param print_logs: should the program print its progress? (e.g. 'file XXX processed)
        :param excluded_items: directories & files to exclude
        """
        self._directory = directory
        self._file_extensions = file_extensions
        self._print_logs = print_logs
        self._excluded_items = excluded_items

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


def format_to_kilobytes(total_bytes):
    """
    convert the given number of bytes to kilobytes and round to 2 decimal digits

    :param total_bytes: number of bytes to convert and format
    :return: converted kilobytes rounded to 2 decimal digits
    """
    kilobytes = total_bytes / 1024
    return round(kilobytes, 2)


def format_extensions(file_extensions):
    """
    format set of file extensions for printing

    :param file_extensions: set of file extensions
    """
    dot_prefixed_extensions = map(lambda e: f'.{e}', file_extensions)
    return ", ".join(dot_prefixed_extensions)


def config_args():
    """
    configure the command line arguments of the program

    :return: parsed script arguments
    """
    parser = ArgumentParser(description='Calculate the total size (both kB and lines of code) of program\'s code.')
    parser.add_argument('-d', '--directory', type=str, required=True)
    parser.add_argument('-e', '--extension', nargs='+', required=True, default=[])
    parser.add_argument('-l', '--log', default=False, action='store_true')
    parser.add_argument('-x', '--exclude', nargs='+', default=[])
    return parser.parse_args()


def main():
    args = config_args()
    file_extensions = tuple(args.extension)
    excluded_items = tuple(map(lambda ex: os.path.join(args.directory, ex), args.exclude))

    code_size_counter = CodeSizeCounter(args.directory, file_extensions, args.log, excluded_items)
    code_size = code_size_counter.calculate_size()

    print('=' * 60)
    print(f'Total {format_extensions(file_extensions)} files: {code_size.total_files}')
    print(f'Total size of {format_extensions(file_extensions)} files: {format_to_kilobytes(code_size.total_size)} kB')
    print(f'Total lines of code: {code_size.total_lines}')
    print('=' * 60)


if __name__ == '__main__':
    main()

import os
from argparse import ArgumentParser

from file_tools import FileSetInfo, FileManager, get_path_with_slashes


class DirectoryInspector:

    def __init__(self, directory, file_extension, debug_prints, excluded_items):
        self._directory = directory
        self._file_extension = file_extension
        self._debug_prints = debug_prints
        self._excluded_items = excluded_items

    def inspect(self):
        return self._inspect(self._directory)

    def _inspect(self, directory):
        """
        inspect the given directory and count lines & size of all files with the given file extension
        """

        # if it's in excluded files/directories, return
        if self._is_excluded(directory):
            return FileSetInfo.empty()

        items = os.listdir(directory)
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        directories = [d for d in items if os.path.isdir(os.path.join(directory, d))]

        file_set_info = FileSetInfo.empty()

        for sub_dir in directories:
            directory_path = os.path.join(directory, sub_dir)
            directory_size = self._inspect(directory_path)
            file_set_info.add(directory_size)

        for file in files:
            file_path = os.path.join(directory, file)
            file_manager = FileManager(file_path)
            if (not file_manager.has_extension(self._file_extension)) or self._is_excluded(file_path):
                continue

            file_info = FileSetInfo(file_manager.get_size(), file_manager.get_lines_count(), 1)
            file_set_info.add(file_info)

            if self._debug_prints:
                print(f'{get_path_with_slashes(file_path)} processed')

        return file_set_info

    def _is_excluded(self, path):
        return any(os.path.samefile(path, ex) for ex in self._excluded_items)


def format_to_kilobytes(total_bytes):
    """
    convert the given number of bytes to kilobytes and round to 2 decimal digits

    :param total_bytes: number of bytes to convert and format
    :return: converted kilobytes rounded to 2 decimal digits
    """
    kilobytes = total_bytes / 1024
    return round(kilobytes, 2)


def config_args():
    """
    configure the command line arguments of the program

    :return: parsed script arguments
    """
    parser = ArgumentParser(description='Calculate the total size (both kB and lines of code) of program\'s code.')
    parser.add_argument('-d', '--directory', type=str, required=True)
    parser.add_argument('-e', '--extension', type=str, required=True)
    parser.add_argument('-l', '--log', default=False, action='store_true')
    parser.add_argument('-x', '--exclude', nargs='+', default=[])
    return parser.parse_args()


def main():
    args = config_args()
    file_extension = args.extension
    excluded_items = tuple(map(lambda ex: os.path.join(args.directory, ex), args.exclude))

    dir_insp = DirectoryInspector(args.directory, file_extension, args.log, excluded_items)
    code_size = dir_insp.inspect()

    print('=' * 60)
    print(f'Total files: {code_size.total_files}')
    print(f'Total size of .{file_extension} files: {format_to_kilobytes(code_size.total_size)} kB')
    print(f'Total lines of code: {code_size.total_lines}')
    print('=' * 60)


if __name__ == '__main__':
    main()

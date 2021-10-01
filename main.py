import sys

from file_tools import inspect_directory
from argparse import ArgumentParser


def format_to_kilobytes(total_bytes):
    kilobytes = total_bytes / 1024
    return round(kilobytes, 2)


def config_args():
    parser = ArgumentParser(description='Calculate the total size (both kB and lines of code) of program\'s code.')
    parser.add_argument('--folder', type=str, required=True)
    parser.add_argument('--extension', type=str, required=True)
    parser.add_argument('--trace', default=False, action='store_true')
    return parser.parse_args()


def main():
    args = config_args()

    file_extension = args.extension
    directory_path = args.folder.replace('\\', '/')

    directory_size = inspect_directory(directory_path, file_extension, args.trace)
    print(f'Total size of .{file_extension} files: {format_to_kilobytes(directory_size.size)} kB')
    print(f'Total lines of code: {directory_size.lines}')


if __name__ == '__main__':
    main()

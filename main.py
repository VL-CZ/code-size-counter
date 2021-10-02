from argparse import ArgumentParser
from file_tools import inspect_directory


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
    parser.add_argument('-f', '--folder', type=str, required=True)
    parser.add_argument('-e', '--extension', type=str, required=True)
    parser.add_argument('-t', '--trace', default=False, action='store_true')
    parser.add_argument('-x', '--exclude', type=str)
    return parser.parse_args()


def main():
    args = config_args()

    file_extension = args.extension
    directory_path = args.folder

    directory_size = inspect_directory(directory_path, file_extension, args.trace)
    print(f'Total size of .{file_extension} files: {format_to_kilobytes(directory_size.size)} kB')
    print(f'Total lines of code: {directory_size.lines}')


if __name__ == '__main__':
    main()

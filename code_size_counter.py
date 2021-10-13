import os
from argparse import ArgumentParser

from src.code_size_counter import CodeSizeCounter


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
    parser = ArgumentParser(
        description='Calculate the total size (both kB and lines of code) of program\'s code.')
    parser.add_argument('-d', '--directory', type=str, required=True,
                        help='Path to the directory where to search files. The path can be either absolute or '
                             'relative.')
    parser.add_argument('-e', '--extension', nargs='+', required=True, default=[],
                        help='extensions of the files that we\'re searching (separated by spaces). Do not prefix them '
                             'with a dot (e.g. use "py" instead of ".py")')
    parser.add_argument('-l', '--log', default=False, action='store_true',
                        help='If present, the program prints its progress (e.g. \'file XXX processed\')')
    parser.add_argument('-x', '--exclude', nargs='+', default=[],
                        help='path to directories & files to exclude (separated by spaces). These paths are relative '
                             'to the given directory (-d parameter)')
    parser.add_argument('-p', '--print', choices=['kb_size', 'lines', 'files'],
                        help='Print just the selected value (kB size, total files or lines of code)')
    return parser.parse_args()


def main():
    args = config_args()
    file_extensions = tuple(args.extension)
    excluded_items = tuple(
        map(lambda ex: os.path.join(args.directory, ex), args.exclude))

    code_size_counter = CodeSizeCounter(
        args.directory, file_extensions, args.log, excluded_items)
    code_size = code_size_counter.calculate_size()

    what_to_print = args.print
    if what_to_print == 'kb_size':
        print(format_to_kilobytes(code_size.total_size))
    elif what_to_print == 'lines':
        print(code_size.total_lines)
    elif what_to_print == 'files':
        print(code_size.total_files)
    else:
        # print all
        print('=' * 60)
        print(
            f'Total {format_extensions(file_extensions)} files: {code_size.total_files}')
        print(
            f'Total size of {format_extensions(file_extensions)} files: {format_to_kilobytes(code_size.total_size)} kB')
        print(f'Total lines of code: {code_size.total_lines}')
        print('=' * 60)


if __name__ == '__main__':
    main()

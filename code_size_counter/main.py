from functools import reduce
import os
from argparse import ArgumentParser

from prettytable import FRAME, PrettyTable


from code_size_counter.code_size_counter import CodeSizeCounter
from code_size_counter.file_tools import NO_EXTENSION_PLACEHOLDER, FileSetSize


def format_to_kilobytes(total_bytes):
    """
    convert the given number of bytes to kilobytes and round to 2 decimal digits

    :param total_bytes: number of bytes to convert and format
    :return: converted kilobytes rounded to 2 decimal digits
    """
    kilobytes = total_bytes / 1024
    return round(kilobytes, 2)


def format_extension(ext):
    """
    Format the given file extension

    :param ext:
    """
    return ext if ext == NO_EXTENSION_PLACEHOLDER else f".{ext}"


def config_args():
    """
    configure the command line arguments of the program

    :return: parsed script arguments
    """
    parser = ArgumentParser(
        description="Calculate the total size (both KB and lines of code) of program's code."
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        required=True,
        help="Path to the directory where to search files. The path can be either absolute or "
        "relative.",
    )
    parser.add_argument(
        "-e",
        "--extension",
        nargs="+",
        default=[],
        help="extensions of the files that we're searching (separated by spaces). Do not prefix them "
        'with a dot (e.g. use "py" instead of ".py"). Leave empty if you search for all files regardless of their extension.',
    )
    parser.add_argument(
        "-l",
        "--log",
        default=False,
        action="store_true",
        help="If present, the program prints its progress (e.g. 'file XXX processed')",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        nargs="+",
        default=[],
        help="path to directories & files to exclude (separated by spaces). These paths are relative "
        "to the given directory (-d parameter)",
    )
    parser.add_argument(
        "-p",
        "--print",
        choices=["kb_size", "lines", "files"],
        help="Print just the selected value (KB size, total files or lines of code)",
    )
    return parser.parse_args()


def main():
    args = config_args()
    file_extensions = tuple(args.extension)
    excluded_items = tuple([os.path.join(args.directory, ex) for ex in args.exclude])

    code_size_counter = CodeSizeCounter(
        args.directory, file_extensions, args.log, excluded_items
    )

    file_sizes = code_size_counter.calculate_size()
    total_sizes = (
        reduce(lambda x, y: x + y, file_sizes.values())
        if file_sizes
        else FileSetSize.empty()
    )

    what_to_print = args.print
    if what_to_print == "kb_size":
        print(format_to_kilobytes(total_sizes.total_size))
    elif what_to_print == "lines":
        print(total_sizes.total_lines)
    elif what_to_print == "files":
        print(total_sizes.total_files)
    else:
        # create results table
        results_table = PrettyTable()
        results_table.field_names = [
            "Extension",
            "Total files",
            "Total lines",
            "Total size (KB)",
        ]
        results_table.vrules = FRAME

        for fn in results_table.field_names:
            results_table.align[fn] = "r"

        # sort by file extension
        file_sizes = dict(sorted(file_sizes.items()))

        for ext, size in file_sizes.items():
            is_last_index = ext == list(file_sizes.keys())[-1]
            results_table.add_row(
                [
                    format_extension(ext),
                    size.total_files,
                    size.total_lines,
                    format_to_kilobytes(size.total_size),
                ],
                divider=is_last_index,
            )

        if len(file_sizes) > 1:
            results_table.add_row(
                [
                    "TOTAL",
                    total_sizes.total_files,
                    total_sizes.total_lines,
                    format_to_kilobytes(total_sizes.total_size),
                ]
            )

        # print the table
        print(results_table)


if __name__ == "__main__":
    main()

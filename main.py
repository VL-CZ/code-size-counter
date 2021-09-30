import sys

from file_tools import inspect_directory


def format_to_kilobytes(total_bytes):
    kilobytes = total_bytes / 1024
    return round(kilobytes, 2)


def main():
    file_extension = sys.argv[2]
    directory_path = sys.argv[1].replace("\\", "/")
    directory_size = inspect_directory(directory_path, file_extension)
    print(f"Total size of .{file_extension} files: {format_to_kilobytes(directory_size.size)} kB")
    print(f"Total lines of code: {directory_size.lines}")


if __name__ == "__main__":
    main()

import os


class FileSystemNodeInfo:
    def __init__(self, size, lines):
        self.size = size
        self.lines = lines


def get_file_size(file_name):
    return os.path.getsize(file_name)


def get_lines_count(file_name):
    with open(file_name, 'r') as file:
        return sum(1 for _ in file)


def has_extension(file_name, extension):
    return file_name.endswith(f'.{extension}')


def inspect_directory(directory, file_extension, debug_prints):
    items = os.listdir(directory)
    files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
    directories = [f for f in items if os.path.isdir(os.path.join(directory, f))]

    (total_size, total_lines) = (0, 0)

    for d in directories:
        directory_path = os.path.join(directory, d)
        directory_size = inspect_directory(directory_path, file_extension, debug_prints)
        total_size += directory_size.size
        total_lines += directory_size.lines

    for f in files:
        if not has_extension(f, file_extension):
            continue
        file_path = os.path.join(directory, f)
        total_size += get_file_size(file_path)
        total_lines += get_lines_count(file_path)

        if debug_prints:
            print(f'{file_path} processed')

    return FileSystemNodeInfo(total_size, total_lines)

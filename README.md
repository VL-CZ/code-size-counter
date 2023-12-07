[![PyPI version](https://badge.fury.io/py/code-size-counter.svg)](https://badge.fury.io/py/code-size-counter)
![GitHub Actions](https://github.com/VL-CZ/code-size-counter/actions/workflows/ci.yml/badge.svg)

# Code size counter
This repository contains a simple command line utility used for calculating total size (both 
KB and lines of code) of program's code.

## Introduction
The main goal of this program is to calculate total size of a source code.
You need to specify the directory that contains the source code and file extension(s) of the desired files.
(for example `html`, `css` and `js`). 
The script then searches the directory for files with the given file extension(s). It's also possible to exclude selected subdirectories from the search
(this is especially useful for directories like `.venv`, `.git` and so on).
The program typically prints:
- number of files found
- total number of lines in these files (newline at the end of the file isn't counted)
- total size of these files in KB (rounded to 2 decimal places). 1 KB = 1024 bytes

See the usage section for further details.

## Requirements
- Python version >= 3.9
- pip

## Installation
Install via pip
```shell
pip install code-size-counter
```

This installs the program as a local python package and allows you to use `code-size-counter` CLI command.

See the [PyPI](https://pypi.org/project/code-size-counter/) page for release history.

## Usage

Below, you can see list of all possible arguments (you can also get the help by running `code-size-counter -h`). `directory` is the only
one required.

```
usage: main.py [-h] -d DIRECTORY [-e EXTENSION [EXTENSION ...]] [-l] [-x EXCLUDE [EXCLUDE ...]] [-p {kb_size,lines,files}]

Calculate the total size (both KB and lines of code) of program's code.

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to the directory where to search files. The path can be either absolute or relative.
  -e EXTENSION [EXTENSION ...], --extension EXTENSION [EXTENSION ...]
                        extensions of the files that we're searching (separated by spaces). Do not prefix them with a dot (e.g. use "py" instead of ".py"). Leave empty if you search for all files regardless of their extension.
  -l, --log             If present, the program prints its progress (e.g. 'file XXX processed')
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        path to directories & files to exclude (separated by spaces). These paths are relative to the given directory (-d parameter)
  -p {kb_size,lines,files}, --print {kb_size,lines,files}
                        Print just the selected value (KB size, total files or lines of code)
```

The typical usage of this program looks like this (see below). In this case, we're looking for `.py` and `.txt` files in `C:/Users/hacker123/Documents/hacking_app` directory,
except those in `.venv` and `.git` subdirectories.
Note that we don't prefix the file extensions with a dot (e.g. use `py` instead of `.py`).

```shell
code-size-counter -d C:/Users/hacker123/Documents/hacking_app -e py txt -x .venv .git
```
Possible output
```
+---------------------------------------------------------+
| Extension   Total files   Total lines   Total size (KB) |
+---------------------------------------------------------+
|       .py             1            50              1.51 |
|      .txt             1             2              0.03 |
+---------------------------------------------------------+
|     TOTAL             2            52              1.54 |
+---------------------------------------------------------+
```
See also other examples below.

### Examples
#### Example 1
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory.

```shell
code-size-counter -d ./tests/complex-test-dir -e py
```
Output
```
+---------------------------------------------------------+
| Extension   Total files   Total lines   Total size (KB) |
+---------------------------------------------------------+
|       .py            31         13030            462.61 |
+---------------------------------------------------------+
```

#### Example 2
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories.
```shell
code-size-counter -d ./tests/complex-test-dir -e py -x virtualenv src/module1
```
Output
```
+---------------------------------------------------------+
| Extension   Total files   Total lines   Total size (KB) |
+---------------------------------------------------------+
|       .py             8           268              8.26 |
+---------------------------------------------------------+
```

#### Example 3
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories and print logs.
```shell
code-size-counter -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -l
```
Output
```
./tests/complex-test-dir/src/module2/main.py processed
./tests/complex-test-dir/src/module2/__init__.py processed
./tests/complex-test-dir/src/code_size_counter.py processed
./tests/complex-test-dir/src/file_tools.py processed
./tests/complex-test-dir/src/__init__.py processed
./tests/complex-test-dir/tests/test_code_size_counter.py processed
./tests/complex-test-dir/tests/__init__.py processed
./tests/complex-test-dir/code_size_counter.py processed
+---------------------------------------------------------+
| Extension   Total files   Total lines   Total size (KB) |
+---------------------------------------------------------+
|       .py             8           268              8.26 |
+---------------------------------------------------------+   
```

#### Example 4
Calculate the size of `.py`, `.md` and `.yml` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories.
```shell
code-size-counter -d ./tests/complex-test-dir -e py md yml -x virtualenv src/module1
```
Output
```
+---------------------------------------------------------+
| Extension   Total files   Total lines   Total size (KB) |
+---------------------------------------------------------+
|      .yml             1            36              1.16 |
|       .py             8           268              8.26 |
|       .md             1             3              0.14 |
+---------------------------------------------------------+
|     TOTAL            10           307              9.56 |
+---------------------------------------------------------+
```

#### Example 5
Calculate the size of all files (regardless of their extension) inside `./directories/my-dir` directory.
```shell
code-size-counter -d ./directories/my-dir
```

Possible output
```
+----------------------------------------------------------+
|  Extension   Total files   Total lines   Total size (KB) |
+----------------------------------------------------------+
|     (NONE)            73           373             36.54 |
|    .flake8             1             2              0.03 |
| .gitignore             2           140              1.95 |
|        .md             2           204              8.25 |
|        .py            44         13533            477.47 |
|       .yml             2            76              2.34 |
+----------------------------------------------------------+
|      TOTAL           172         16584            623.34 |
+----------------------------------------------------------+
```

Also note the `(NONE)` extension, which means that the file has no extension


#### Example 6
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories 
and print just the number of lines.
```shell
code-size-counter -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -p lines
```

Output
```
268
```

You can then pipe the result (as you can see on the example below).
```shell
code-size-counter -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -p lines | python -c "loc = input(); print(f'I copied {loc} lines from StackOverflow.')"
```
Output
```
I copied 268 lines from StackOverflow.
```

## Developer documentation

We're using [Poetry](https://python-poetry.org/docs/) for dependency management and packaging.

### Program structure

- [code_size_counter](./code_size_counter/) folder - source code files of the program
  - [main.py](code_size_counter/main.py) is the entry-point of the app
- [tests](./tests) folder - unit tests of the program (using `Python unittest` module). The subfolders serve as a test data.

To run the tests, use the following command
```shell
poetry run python -m unittest discover tests -v
```

Run this command in the **root** folder to execute `main.py` as a script.
```shell
poetry run python -m source_code_size_counter.main
```

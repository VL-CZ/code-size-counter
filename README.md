# Source code size counter
This repository contains a simple command line script used for calculating total size (both 
kB and lines of code) of program's code.

## Requirements
- Python version 3. If your `python` command points to older version, use `python3` instead.

## Usage
The main functionality of this program is calculating the total size of a source code.
You need to specify the directory that contains the source code and ...

You can run this program directly from the command line, see the help message below.

```
usage: code_size_counter.py [-h] -d DIRECTORY -e EXTENSION [EXTENSION ...] [-l] [-x EXCLUDE [EXCLUDE ...]] [-p {kb_size,lines,files}]

Calculate the total size (both kB and lines of code) of program's code.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The directory where to search files
  -e EXTENSION [EXTENSION ...], --extension EXTENSION [EXTENSION ...]
                        extensions of the files that we're searching (separated by spaces)
  -l, --log             If present, the program prints its progress (e.g. 'file XXX processed')
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        path to directories & files to exclude (separated by spaces). These paths are relative to the given directory (-d parameter)
  -p {kb_size,lines,files}, --print {kb_size,lines,files}
                        Print just the selected value (kB size, total files or lines of code)
```

Required arguments are:
- -d DIRECTORY
- -e EXTENSION

To show the help, use the following command
```shell
python code_size_counter.py -h
```


```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py
```
Possible output
```
============================================================
Total .py files: 3
Total size of .py files: 9.47 kB
Total lines of code: 615
============================================================
```

See also other examples below.
### Examples
#### Example 1
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory.

```shell
python code_size_counter.py -d ./tests/complex-test-dir -e py
```
Output
```
============================================================
Total .py files: 31
Total size of .py files: 462.61 kB
Total lines of code: 13030
============================================================
```

#### Example 2
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories.
```shell
python code_size_counter.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1
```
Output
```
============================================================
Total .py files: 8
Total size of .py files: 8.26 kB
Total lines of code: 268
============================================================
```

#### Example 3
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories and print logs.
```shell
python code_size_counter.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -l
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
============================================================      
Total .py files: 8
Total size of .py files: 8.26 kB
Total lines of code: 268
============================================================      
```

#### Example 4
Calculate the size of `.py`, `.md` and `.yml` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories and print logs.
```shell
python code_size_counter.py -d ./tests/complex-test-dir -e py md yml -x virtualenv src/module1 -l
```
Output:
```
./tests/complex-test-dir/.github/workflows/python-app.yml processed
./tests/complex-test-dir/src/module2/main.py processed
./tests/complex-test-dir/src/module2/__init__.py processed        
./tests/complex-test-dir/src/code_size_counter.py processed       
./tests/complex-test-dir/src/file_tools.py processed
./tests/complex-test-dir/src/__init__.py processed
./tests/complex-test-dir/tests/test_code_size_counter.py processed
./tests/complex-test-dir/tests/__init__.py processed
./tests/complex-test-dir/code_size_counter.py processed
./tests/complex-test-dir/README.md processed
============================================================
Total .py, .md, .yml files: 10
Total size of .py, .md, .yml files: 9.56 kB
Total lines of code: 307
============================================================
```

#### Example 5
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories 
and print just the number of lines.
```shell
python code_size_counter.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -p lines
```

Output:
```
268
```

You can then pipe the result (as you can see on the example below).
```shell
python code_size_counter.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -p lines | python -c "loc = input(); print(f'I copied {loc} lines from StackOverflow.')"
```
Output
```
I copied 268 lines from StackOverflow.
```

## Developer documentation
### Program structure

- [src](./src) folder - source code files of the program
- [tests](./tests) folder - unit tests of the program (using `Python unittest` module). The subfolders serve as a test data.

To run the tests, use the following command
```shell
python -m unittest discover tests -v
```

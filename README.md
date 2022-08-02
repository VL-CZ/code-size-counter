# Source code size counter
This repository contains a simple command line script used for calculating total size (both 
KB and lines of code) of program's code.

## Introduction
The main goal of this program is to calculate total size of a source code.
You need to specify the directory that contains the source code and file extension(s) of the source code files. You can set multiple file extensions
(for example `html`, `css` and `js`). 
The script then searches the directory for files with the given file extension. You can also exclude selected subdirectories from the search
(this is especially useful for directories like `.venv`, `.git` and so on).
The program typically prints:
- number of files found
- total number of lines in these files (newline at the end of the file isn't counted)
- total size of these files in KB (rounded to 2 decimal places). 1 KB = 1024 bytes

See the usage section for further details.

## Requirements
- Python version 3. If your `python` command points to older version, use `python3` instead.

## Usage

Below, you can see list of all possible arguments (you can also get the help by running `python code_size_counter.py -h`). `Directory` and `extension` are the only
ones that are required.

```
usage: code_size_counter.py [-h] -d DIRECTORY -e EXTENSION [EXTENSION ...] [-l] [-x EXCLUDE [EXCLUDE ...]] [-p {kb_size,lines,files}]

Calculate the total size (both KB and lines of code) of program's code.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to the directory where to search files. The path can be either absolute or relative.
  -e EXTENSION [EXTENSION ...], --extension EXTENSION [EXTENSION ...]
                        extensions of the files that we're searching (separated by spaces). Do not prefix them with a dot (e.g. use "py" instead of ".py")
  -l, --log             If present, the program prints its progress (e.g. 'file XXX processed')
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        path to directories & files to exclude (separated by spaces). These paths are relative to the given directory (-d parameter)     
  -p {kb_size,lines,files}, --print {kb_size,lines,files}
                        Print just the selected value (KB size, total files or lines of code)
```

The typical usage of this program looks like this (see below). In this case, we're looking for `py` files in `C:/Users/hacker123/Documents/hacking_app` directory
except those in `.venv` and `.git` subdirectories.
Note that we don't prefix the file extensions with a dot (e.g. use `py` instead of `.py`).

```shell
python program.py -d C:/Users/hacker123/Documents/hacking_app -e py -x .venv .git
```
Possible output
```
============================================================
Total .py files: 3
Total size of .py files: 9.47 KB
Total lines of code: 615
============================================================
```
See also other examples below.

### Add alias for this script
You can also create PowerShell/Bash alias for this script. 
Then, you can just type `code_size_counter` instead of `python {folder_with_the_script}/code_size_counter.py` to run this script.

#### PowerShell
Add these lines to your PowerShell profile file (it's usually located in `~\Documents\PowerShell\Profile.ps1`). 
For further info, see the [documentation](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles)

```powershell
function run_code_size_counter {
    python {ABSOLUTE_PATH_TO_THE_SCRIPT_FOLDER}\code_size_counter.py $args
}

New-Alias code_size_counter run_code_size_counter
```

#### Bash
Add this line to `~/.bashrc` file.

```bash
alias code_size_counter='python {ABSOLUTE_PATH_TO_THE_SCRIPT_FOLDER}/program.py'
```

### Examples
#### Example 1
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory.

```shell
python program.py -d ./tests/complex-test-dir -e py
```
Output
```
============================================================
Total .py files: 31
Total size of .py files: 462.61 KB
Total lines of code: 13030
============================================================
```

#### Example 2
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories.
```shell
python program.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1
```
Output
```
============================================================
Total .py files: 8
Total size of .py files: 8.26 KB
Total lines of code: 268
============================================================
```

#### Example 3
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories and print logs.
```shell
python program.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -l
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
Total size of .py files: 8.26 KB
Total lines of code: 268
============================================================      
```

#### Example 4
Calculate the size of `.py`, `.md` and `.yml` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories and print logs.
```shell
python program.py -d ./tests/complex-test-dir -e py md yml -x virtualenv src/module1 -l
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
Total size of .py, .md, .yml files: 9.56 KB
Total lines of code: 307
============================================================
```

#### Example 5
Calculate the size of `.py` files inside `./tests/complex-test-dir` directory. Exclude `virtualenv` and `src/module1` subdirectories 
and print just the number of lines.
```shell
python program.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -p lines
```

Output:
```
268
```

You can then pipe the result (as you can see on the example below).
```shell
python program.py -d ./tests/complex-test-dir -e py -x virtualenv src/module1 -p lines | python -c "loc = input(); print(f'I copied {loc} lines from StackOverflow.')"
```
Output
```
I copied 268 lines from StackOverflow.
```

## Developer documentation
### Program structure

- [src](./src) folder - source code files of the program
- [tests](./tests) folder - unit tests of the program (using `Python unittest` module). The subfolders serve as a test data.
- [code_size_counter.py](program.py) is the entry-point of the app

To run the tests, use the following command
```shell
python -m unittest discover tests -v
```

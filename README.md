# Source code size counter
This repository contains a simple command line script used for calculating total size (both 
kB and lines of code) of program's code.

## Requirements

## Usage

```shell
usage: code_size_counter.py [-h] -d DIRECTORY -e EXTENSION [EXTENSION ...] [-l] [-x EXCLUDE [EXCLUDE ...]] [-p {kb_size,lines,files}]

Calculate the total size (both kB and lines of code) of program's code.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The directory where to search files
  -e EXTENSION [EXTENSION ...], --extension EXTENSION [EXTENSION ...]
                        extensions of the files that we're searching
  -l, --log             If present, the program prints its progress (e.g. 'file XXX processed')
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        path to directories & files to exclude. This path is relative to the given directory (-d parameter)
  -p {kb_size,lines,files}, --print {kb_size,lines,files}
                        Print just the selected criteria (kB size, total files or lines of code)
```

`python code_size_counter.py -h`

## Examples

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py
```

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py -l
```

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py -l
```

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py -x .venv .git conf/python-conf
```

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py -x .venv .git conf/scripts
```

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py -x .venv .git conf/scripts
```

```shell
python code_size_counter.py -d C:/Users/hacker123/Documents/hacking_app -e py -x .venv .git conf/scripts
```

## Developer documentation

```shell
python -m unittest discover tests -v
```

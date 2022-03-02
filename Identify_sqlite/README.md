## Identify SQLite files from File Carve
A script to determine the types of SQLite files from a file carve. 
## Usage
```console
$ python3 identify_sqlite.py -h
usage: identify_sqlite.py [-h] -d <path> [-m <path>] [-c <path>]

A simple python script to identify SQLite files that have been carved from a
disk

optional arguments:
  -h, --help            show this help message and exit
  -d <path>, --directory <path>
                        Directory of files to scan
  -m <path>, --move <path>
                        Move Files into sorted directory structure
  -c <path>, --copy <path>
                        Copy Files into sorted directory structure
```
## To Do
- Detect more DB types
- Backwards files? ikr
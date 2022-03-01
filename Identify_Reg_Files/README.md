# Identify Reg files
A script to determine the type of reg file. Currently only Linux based.
## Usage
```console
$ python3 main.py -h
usage: main.py [-h] -d <path> [-o <filename>]

optional arguments:
  -h, --help            show this help message and exit
  -d <path>, --directory <path>
                        Directory of files to scan
  -o <filename>, --output <filename>
                        Place to save the CSV file of results. Default:
                        ./output.csv
```
## To Do
- Rename files after identification as a command line option.
- Identify files that are currently classified as UNKNOWN
- Make Windows and Linux freindly.
## Interesting items
While trying to compleate this I found this pice of reserch here: https://github.com/msuhanov/regf/blob/master/Windows%20registry%20file%20format%20specification.md 

This did change how I worked this all out!
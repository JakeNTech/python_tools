# Identify Reg files
A script to determine the type of reg file. Currently only Linux based.
## Usage
```console
$ python3 main.py -h
usage: main.py [-h] -d <path> [-m <path>] [-c <path>]

A simple python script to identify Windows Registry files that have been
carved from a disk

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
- Rename files after identification as a command line option. -> Done
- Identify files that are currently classified as UNKNOWN
  -> Could be done with RECmd from Eric Zimmerman but would need to run on Windows, or create my own python Parser for Linux (OHH EXCITING!)
- Make Windows and Linux friendly.
  -> Longer term project is to make a program that will enable a user to connect a drive to a Raspberry Pi, and have all identification of files automated. For images, SQLite and Reg files. Mostly to free up my laptop while processing this
## Interesting items
While trying to complete this I found this pice of research here: https://github.com/msuhanov/regf/blob/master/Windows%20registry%20file%20format%20specification.md 

This did change how I worked this all out!
# File Hasher Virus Total Script
A script to list out files in a given directory, calculate the hash and scan the file on Virus Total.\
Uses SHA256.
## Usage
```console
$ python3 main.py -d ./test_files -k <Virus_Total_API_Key>
```
## Options
```console
  -h, --help            show this help message and exit
  -d <path>, --directory <path>
                        Directory of files
  -k <key>, --key <key>
                        api_key
  -p <key>, --pass <key>
                        text file containing known hashes
  -o <filename>, --output <filename>
                        Place to save the CSV file of results
```
## Notes
Currently only supports one directory.
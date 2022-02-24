# zip-brute-force
Brute force the password to a zip file using a word list

## Usage
`$ python3 brute.py -f <zip_file_path/name> -w <wordlist_path/name>`

## Options
-n, --number <number_of_numbers>\
Using this option will append a number (upto the max_number selected) to the end of the password, e.g:
```
password11
password12
...
```
-l, --letters <number_of_chars>\
Using this option will append letters (upto the max_number) to the end of the password, e.g:
```
passwordaa
passwordab
...
```
-s, --symbols <number_of_chars>\
Using this option will append symbols (upto the max_number) to the end of the password e.g:
```
password!!
password!"
...
```
-a , --all <number_of_chars>\
Using this optin will apped Letter, Numbers and Symbols to the end of a password.


Proberbly not the best/most useful script in the world, but it might do what you want it to do
# Bookmarks

Bookmarks is a python program that outputs json from a Netscape Bookmarks File (or multiple files) exported from firefox, Chrome (untested)

## Installation
Source and Binary distribution is available in the release section    
Binary installation:    
```pip install binary_name.whl```

## Usage   

`python -m bookmarks \`
 `--file [INPUT_FILE] \`
 `--output [OUTPUT_FILE]`    

Examples: 
- ```python -m bookmarks --file file1 --file file 2 --output something.json``` 
- ```python -m bookmarks -f /home/user/important_data/bookmarks.html -o /home/file.json``` 

Note: 
- Short forms `-f` for `--files` and `-o` for `--output` available    
- If no input file is provided, the program will look for bookmarks.html in the current folder    
- If no output file is provided, the program will output bookmarks.json in the current folder    
- Multiple input files are supported in which case, the program will merge all bookmarks
- In case of multiple files with conflict, clashing data from older files will be overwritten with the data from newer files

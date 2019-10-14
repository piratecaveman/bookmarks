# Bookmarks

Bookmarks is a python program that outputs json from a Netscape Bookmarks File exported from firefox, Chrome (untested)

## Installation
Source and Binary distribution is available in the release section    
Binary installation:    
```pip install binary_name.whl```

## Usage   

`python -m bookmarks --file [INPUT_FILE] --output [OUTPUT_FILE]`    

Examples:    
```python -m bookmarks -f bookmarks.html -o bookmarks.json```    
```python -m bookmarks --file bookmarks.html --output bookmarks.json```    
```python -m bookmarks --file C:\Users\me_an_intelectual\bookmarks.html --output D:\trash\bookmarks.json```    
```python -m bookmarks -f /home/user/important_data/bookmarks.html -o /home/file.json```    

Short forms `-f` for `--files` and `-o` for `--output` available    
If no input file is provided, the program will look for bookmarks.html in the current folder    
If no output file is provided, the program will output bookmarks.json in the current folder    

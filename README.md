# python-file-shredder
Python program to shred file(s) and directories

# python-file-shredder

## Usage
CLI Program to take in either a file pattern `-f FILE` or `--file FILE` or a directory `-d DIRECTORY` or `--directory DIRECTORY` (along with a root directory to start searching from `-s SEARCH_PATH` or  `--search-path SEARCH_PATH`), and will overwrite data a specified number of times `-p [PASSES]` or `--passes [PASSES]` with random bytes. After the specified number of passes the file will be overwritten with bytes `x\00`, raw `b'00'`. After the final overwrite (finished shredding), the file will then be deleted. For directories, this will recursively shred through files in the subdirectories, and then remove the directory and subdirectories from the system as well.

## Current Development Info
Currently the recursive directory shredding/removal is not fully built, so I would advise to only use for sjredding specific files (which is probably safer anyways so you don't accidentally remove important files within a directory). 

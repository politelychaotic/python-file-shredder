import os
import fnmatch

'''
Library for finding files in filesystem starting at a specified root directory.
Usage: Use with a Python script that requires searching for files on the filesystem.
Author: PolitelyChaotic
Date: August 13, 2024

Usage:

print(find_file('{filename.extension}', '/Users/{user}/home/'))
print(find_files_with_fnmatch('/Users/{user}/home/', '{filename.extension}'))
'''

def find_file(filename, search_path):
    file_list = []
    #walk top-down from root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list

def find_files_with_fnmatch(search_path, target_pattern):
    found_files = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if fnmatch.fnmatch(file, target_pattern):
                found_files.append(os.path.join(root, file))
    return found_files
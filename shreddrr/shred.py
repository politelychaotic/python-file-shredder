#!/bin/python

import os, time, sys, string, random
import argparse
import shutil
from find_files import find_files_with_fnmatch

delay = 0.5
separate_str = "--------------------"


cat = """
                                               .--.
                                               `.  \\
                                                 \  \\
                                                  .  \\
                                                  :   .
                                                  |    .
                                                  |    :
                                                  |    |
  ..._  ___                                       |    |
 `."".`''''""--..___                              |    |
 ,-\  \             ""-...__         _____________/    |
 / ` " '                    `""\""\""\""                  .
 \                                                      L
 (>                                                      \\
/                                                         \\
\_    ___..---.                                            L
  `--'         '.                                           \\
                 .                                           \_
                _/`.                                           `.._
             .'     -.                                             `.
            /     __.-Y     /''''''-...___,...--------.._            |
           /   _."    |    /                ' .      \   '---..._    |
          /   /      /    /                _,. '    ,/           |   |
          \_,'     _.'   /              /''     _,-'            _|   |
                  '     /               `-----''               /     |
                  `...-'                                       `...-'
                  shred.py
                  File shredder by PolitelyChaotic
                  August 13, 2024
"""

dir_char = "/"
if(os.name == "nt"):
    dir_char = '\\'

sub_dirs = []
file_list = []

def cont():
    cont = input("[WARNING] You may not be able to recover the selected file(s). Continue? (y/n): ")
    if((cont == 'n' or cont == 'N')or (cont != 'n' and cont != 'N' and cont != 'y' and cont != 'Y')):
        print("[*] Exiting...")
        exit(0)

def iterate_subdir():
    global file_list
    for dir in sub_dirs:
        file_list += [f"{dir}{dir_char}{file}" for file in os.listdir(dir) if os.path.isfile(f"{dir}{dir_char}{file}")]

def find_subdirs(directory : str, passes : int):
    global sub_dirs
    if(os.path.isdir(directory) == True):
        for dir in next(os.walk(directory))[1]:
            sub_dirs.append(f"{dir}{dir_char}{dir}") # Loop through sub dirs
    else:
        print("[!] The directory \"{dir}\" is not valid")
        print("[+] Directories validated")
    return sub_dirs

def shred_file(path : str, passes : int):
    print(f"[*] Shredding: {path}")
    valid_chars = string.ascii_letters + string.digits
    valid_bytes = [chr(c) for c in range(0xFF+1)]
    #print(valid_bytes)
    raw_byte_encode = "latin1"
    #print(random.choice(valid_bytes).encode(raw_byte_encode))
    filesize = os.path.getsize(path)
    print(f'[i] Filesize: {filesize}')
    if(os.path.isfile(path) == True and filesize > 0):
        for temp in range(passes):
            #overwrite file with random raw bytes
            for i in range(filesize):
                fd = os.open(path, os.O_WRONLY|os.O_NOCTTY)
                os.pwrite(fd, random.choice(valid_bytes).encode(raw_byte_encode), i)

        time.sleep(delay)
        print(f'[+] {path} shredded')
        print(separate_str)
        print(f'[*] Overwriting {path} with zeroes...')
        for i in range(filesize):
            os.pwrite(fd, b'0', i)

        time.sleep(delay)
        print(f'[+] {path} is zeroed')
        time.sleep(delay)
        print(separate_str)
        os.close(fd)

    # Delete file after shredding and filling with zeroes
    '''print(f'[*] Deleting {path}...')
    os.remove(path)
    time.sleep(delay)
    print(f'[+] {path} deleted')'''

def shred_dirs(directory : str, passes : int):
    #Shred all valid files
    if(len(file_list) > 0):
        print("[*] Shredding files...")
        for file in file_list:
            try:
                shred_file(file, passes)
            except:
                print(f"[!] Exception raised while shredding file \"{file}\"")
                print(f"[i] Exception info: {sys.exc_info()[0]}")
        print("[+] Files shredded")

        if(len(sub_dirs) > 0):
            print("[*] Removing directories...")
            for dir in sub_dirs:
                shutil.rmtree(dir, ignore_errors=True)
            print("[+] Directories removed")
    else:
        print("[!] No files to shred")
        

if __name__ == '__main__':
    print(cat)
    time.sleep(delay * 2)
    print("<< shred.py >>")
    print(separate_str * 4)
    time.sleep(delay)
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", action="store", help="specify directories to shred", dest="directory", default="")
    parser.add_argument("-f", "--files", action="store", nargs="+", help="specify files to shred", dest="files", default='')
    parser.add_argument("-s", "--search-path", type=str, action="store", dest="search_path", help="Root path to find files from", default="/Users/")
    parser.add_argument("-p", "--passes", type=int, action="store", nargs="?", help="specify the amount of passes", dest="passes", default="4")
    args = parser.parse_args()
    if len(args.files[0]) < 1 and not args.directory:
        # No files are specified and there is no specified directory
        print('\n')
        parser.print_help()
        print('\n')
        exit(0)
        
    try:
        files = args.files
        directory = args.directory
        passes = args.passes
        search_path = args.search_path

        #print(args)
        #print(f'Search path is a directory? {os.path.isdir(search_path)}')
        
        if(directory):
            print(f"[i] Directory to shred: {directory}")
            time.sleep(delay)
    
        print(f"[i] Number of passes: {passes}")
        time.sleep(delay)

        if(passes <= 0 or (files == "" and directory == False)):
            parser.print_help()
            print(args)
            exit(0)
    except SystemExit:
        exit(0)
    except:
        print("[!] Unable to parse arguments!")
        parser.print_help()
        exit(0)

    try:
        pos = 0
        print(f"[i] Matching file names: {files}")
        print(separate_str)
        for file in files:
            if os.path.isfile(file):
                file_list = find_files_with_fnmatch(search_path, file)
            time.sleep(delay)
        print(f'[i] File list: {file_list}')

        filepath = file_list[pos]
        
        if len(file_list) > 1:
            file_to_shred = int(input("Please enter a positional number for picking\nwhich file to shred (starting at 0): "))
            filepath = file_list[pos]
            print(separate_str)
            time.sleep(delay)
            cont()
            time.sleep(delay)
            shred_file(filepath, passes)

        elif len(file_list) == 1:
            cont()
            time.sleep(delay)
            shred_file(filepath, passes)
        elif directory:
            print('directory deletion chosen.')
            d
    except KeyboardInterrupt:
        print("[!] Interrupted, exiting...")
        exit(0)
    except:
        print(f"[!] Exeception raised: {sys.exc_info()[0]}\nexiting...")
        exit(0)
    

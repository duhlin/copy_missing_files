# copy_missing_files
Simple python script which copies all files from a given directory that do not already exist in target directory.
usage: copy_missing.py [-h] [--list] [--diagnostic] [--use_md5]
                       [--subfolder SUBFOLDER]
                       src [src ...] dest

```
copy file from src which are missing from dest.

positional arguments:
  src                   source files or directories
  dest                  destination directory

optional arguments:
  -h, --help            show this help message and exit
  --list                list files from src which are missing from dest.
                        (default: copy)
  --diagnostic          displays a report of both found and not found files
  --use_md5             use md5 hash and size to compare file instead of using
                        file names.
  --subfolder SUBFOLDER
                        copy in dest/subfolder. (default: dest)
```

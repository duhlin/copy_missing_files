#!/usr/bin/python

import argparse
import shutil
import os
import md5

def get_md5(filename, size=None):
   m = md5.new()
   f = open(filename, 'rb')
   m.update(f.read(size))
   return m.hexdigest()

def get_size_and_md5(filename):
  return (os.stat(filename).st_size, get_md5(filename, 4095))

class FileList:
    def __init__(self):
        self.fileList = dict()
        self.getFileId = os.path.basename

    def load(self, directory):
        for root, dirs, files in os.walk( directory ):
            for f in files:
                file_path = os.path.join(root,f)
                try:
                    file_id = self.getFileId( file_path )
                    if file_id in self.fileList:
                        self.fileList[ file_id ].append( file_path )
                    else:
                        self.fileList[ file_id ] = [ file_path ]
                except (IOError, OSError) as e:
                    print "I/O error({0}): ignoring file {1}".format(e, file_path)

    def find_missing(self, directory):
        ret = []
        for root, dirs, files in os.walk( directory ):
            for f in files:
                file_path = os.path.join(root,f)
                file_id = self.getFileId( file_path )
                if file_id in self.fileList:
                    ret.append( (file_path, True, self.fileList[file_id]) )
                else:
                    ret.append( (file_path, False, []) )
        return ret

def diagnostic(filename, found, where):
    if found:
        print os.path.join(src, filename), 'found in', where
    else:
        print os.path.join(src, filename), 'not found'

def print_missing_only(filename, found, where):
    if not found:
        print filename

class FileCopier:
    def __init__(self, base_directory):
        self.baseDirectory = base_directory
        self.create_basedirectory()

    def create_basedirectory(self):
        try:
            os.mkdir( self.baseDirectory )
        except OSError:
            pass #directory already exists

    def copy_missing_only(self, filename, found, where):
        if not found:
            if os.path.exists( os.path.join(self.baseDirectory, os.path.basename(filename)) ):
                print "Warning: {0} already exists in {1}. Skip copy".format(os.path.basename(filename), self.baseDirectory)
            else:
                print "cp -p", filename, self.baseDirectory
                shutil.copy2(filename, self.baseDirectory) # copy2: with metadata

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='copy file from src which are missing from dest.')
    parser.add_argument('--list', action="store_true", default=False, help='list files from src which are missing from dest. (default: copy)')
    parser.add_argument('--diagnostic', action="store_true", default=False, help='displays a report of both found and not found files')
    parser.add_argument('--use_md5', action="store_true", default=False, help='use md5 hash and size to compare file instead of using file names.')
    parser.add_argument('src', nargs='+', help='source files or directories')
    parser.add_argument('dest', nargs=1, help='destination directory')
    parser.add_argument('--subfolder', default='', help='copy in dest/subfolder. (default: dest)')
    args = parser.parse_args()

    if args.list:
        report = print_missing_only
    elif args.diagnostic:
        report = diagnostic
    else:
        base_dir = os.path.join(args.dest[0], args.subfolder)
        copier = FileCopier( base_dir )
        report = copier.copy_missing_only

    if not os.path.isdir( args.dest[0] ):
        raise IOError( args.dest[0] ) 

    file_list = FileList()
    if args.use_md5:
        file_list.getFileId = get_size_and_md5
    
    file_list.load( args.dest[0] )

    for src in args.src:
        if not os.path.exists( src ):
            raise IOError( src ) 
        else:
            for (filename, found, where) in file_list.find_missing( src ):
                report( filename, found, where )
    


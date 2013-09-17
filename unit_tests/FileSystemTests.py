"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from tools.FileSystem import FileSystem
import os
import unittest

class FileSystemTests(unittest.TestCase):

    def test_file_not_exists1(self):
        filename = "./temp.bin"
        try:
            os.remove(filename)
        except OSError:
            pass
        
        self.assertFalse(FileSystem.file_exists_new_shell(filename))
        
    def test_file_exists1(self):
        filename = "./temp.bin"
        f = open(filename, 'w')
        f.close()
        self.assertTrue(FileSystem.file_exists_new_shell(filename))
        
        try:
            os.remove(filename)
        except OSError:
            pass
        
    def test_file_not_exists2(self):
        filename = "temp.bin"
        try:
            os.remove(filename)
        except OSError:
            pass
        
        self.assertFalse(FileSystem.file_exists_new_shell(filename))
        
    def test_file_exists2(self):
        filename = "temp.bin"
        f = open(filename, 'w')
        f.close()
        self.assertTrue(FileSystem.file_exists_new_shell(filename))
        
        try:
            os.remove(filename)
        except OSError:
            pass
        
    def test_get_unique_filename(self):
        for _ in range(100):
            fn = FileSystem.get_unique_filename("")
            self.assertFalse(os.path.exists(fn))
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

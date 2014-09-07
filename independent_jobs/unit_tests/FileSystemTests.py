"""
Copyright (c) 2013-2014 Heiko Strathmann
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 *
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 *
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the author.
"""
import os
import tempfile
import unittest

from independent_jobs.tools.FileSystem import FileSystem


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
            
    def test_delete_dir_failsafe(self):
        # create dir
        dirname = tempfile.mkdtemp()
        try:
            os.mkdir(dirname)
        except OSError:
            pass
        self.assertTrue(os.path.isdir(dirname))
        
        # put a file to have a non empty dir
        open(os.sep.join([dirname, 'temp']), 'a').close()
        
        # delete and make sure it works
        FileSystem.delete_dir_failsafe(dirname)
        self.assertFalse(os.path.isdir(dirname))
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

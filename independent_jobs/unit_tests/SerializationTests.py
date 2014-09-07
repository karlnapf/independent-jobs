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
import unittest

from independent_jobs.tools.Serialization import Serialization


class SerializationTests(unittest.TestCase):

    def test_serialize_object_file_exists(self):
        filename = "temp.bin"
        obj = [1, 2, 3]
        with self.assertRaises(OSError):
            Serialization.serialize_object(obj, filename)
            Serialization.serialize_object(obj, filename)
        
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)
        
    def test_serialize_object_file_not_exists(self):
        filename = "temp.bin"
        obj = [1, 2, 3]
        
        try:
            os.remove(filename)
        except OSError:
            pass
        
        Serialization.serialize_object(obj, filename)
        self.assertTrue(os.path.exists(filename))
        
    def test_serialize_and_deserialize(self):
        filename = "temp.bin"
        obj = [1, 2, 3]
        
        Serialization.serialize_object_overwrite(obj, filename)
        obj2 = Serialization.deserialize_object(filename)
        
        self.assertEqual(obj, obj2)
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

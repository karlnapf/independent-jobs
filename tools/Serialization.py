"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from pickle import dump, load
import os

class Serialization(object):
    @staticmethod
    def serialize_object(obj, filename):
        
        # race condition doesn't not matter since we are doing nothing if file
        # exists and overwrite if it was created in the meantime
        if os.path.exists(filename):
            raise OSError("File \"" + filename + "\" already exists. Overwriting")
            
        Serialization.serialize_object_overwrite(obj, filename)
            
    @staticmethod
    def serialize_object_overwrite(obj, filename):
        f = open(filename, 'wb')
        dump(obj, f)
        f.close()
        
    @staticmethod
    def deserialize_object(filename):
        f = open(filename, 'rb')
        obj = load(f)
        f.close()
        
        return obj


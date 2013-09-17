"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
import os
import subprocess
import uuid

class FileSystem(object):
    @staticmethod
    def file_exists_new_shell(filename):
        """
        Spawns a new python shell to check file existance in context of NFS
        chaching which makes os.path.exists lie. This is done via a pipe and the
        "ls" command
        """
        
        # split path and filename
        splitted = filename.split(os.sep)
        
        if len(splitted) > 1:
            folder = os.sep.join(splitted[:-1]) + os.sep
            fname = splitted[-1]
        else:
            folder = "./"
            fname = filename
        
        pipeoutput = subprocess.Popen("ls " + folder, shell=True, stdout=subprocess.PIPE)
        pipelines = pipeoutput.stdout.readlines()
        files = "".join(pipelines).split(os.linesep)
        return fname in files

    @staticmethod
    def get_unique_filename(filename_base):
        while True:
            fn = filename_base + unicode(uuid.uuid4())
            try:
                open(fn, "r")
            except IOError:
                # file did not exist, use that filename
                break
        return fn

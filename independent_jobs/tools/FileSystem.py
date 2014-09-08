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
import shutil
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

    @staticmethod
    def delete_dir_failsafe(folder):
        try:
            shutil.rmtree(folder)
        except OSError:
            pass
        
    @staticmethod
    def cmd_exists(cmd):
        return subprocess.call("type " + cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

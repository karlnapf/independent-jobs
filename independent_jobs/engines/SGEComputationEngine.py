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
import time

from independent_jobs.engines.BatchClusterComputationEngine import BatchClusterComputationEngine


class SGEComputationEngine(BatchClusterComputationEngine):
    def __init__(self, batch_parameters, check_interval=10):
        BatchClusterComputationEngine.__init__(self, batch_parameters, check_interval)

    def create_batch_script(self, job_name, dispatcher_string):
        command = dispatcher_string
        
        walltime = time.strftime('%H:%M:%S', time.gmtime(self.batch_parameters.max_walltime))
        
        memory = str(self.batch_parameters.memory) + "G"
        workdir = self.get_job_foldername(job_name)
        
        output = workdir + os.sep + "output.txt"
        error = workdir + os.sep + "error.txt"

        job_string = \
"""#$ -S /bin/bash
#$ -N %s
#$ -l h_rt=%s
#$ -l h_vmem=%s,tmem=%s
#$ -o %s
#$ -e %s
#$ -wd %s
source ~/.bash_profile
%s""" % (job_name, walltime, memory, memory, output, error, workdir, command)
        
        return job_string

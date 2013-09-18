"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from engines.BatchClusterComputationEngine import BatchClusterComputationEngine
import os
import time

class SGEComputationEngine(BatchClusterComputationEngine):
    def __init__(self, batch_parameters, check_interval=10):
        BatchClusterComputationEngine.__init__(self, batch_parameters, check_interval)

    def create_batch_script(self, job_name, dispatcher_string):
        command = dispatcher_string
        
        walltime = time.strftime('%H:%M:%S', time.gmtime(self.batch_parameters.max_walltime))
        walltime = walltime
        
        memory = str(self.batch_parameters.memory) + "G"
        workdir = self.get_job_foldername(job_name)
        
        output = workdir + os.sep + "output.txt"
        error = workdir + os.sep + "error.txt"

        job_string = """
#$ -S /bin/bash
source ~/.bash_profile
#$ -N %s
#$ -l h_rt=%s
#$ -l h_vmem=%s,tmem=%s
#$ -o %s
#$ -e %s
#$ -wd %s
%s""" % (job_name, walltime, memory, memory, output, error, workdir, command)
        
        return job_string

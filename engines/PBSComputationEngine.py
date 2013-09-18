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

class PBSComputationEngine(BatchClusterComputationEngine):
    def __init__(self, batch_parameters, check_interval=10):
        BatchClusterComputationEngine.__init__(self, batch_parameters, check_interval)

    def create_batch_script(self, job_name, dispatcher_string):
        command = "nice -n 10 " + dispatcher_string
        
        walltime = time.strftime('%H:%M:%S', time.gmtime(self.batch_parameters.max_walltime))
        walltime = "walltime=" + walltime
        
        num_nodes = "nodes=1:ppn=" + str(self.batch_parameters.nodes)
        memory = "pmem=" + str(self.batch_parameters.memory) + "gb"
        workdir = self.get_job_foldername(job_name)
        
        output = workdir + os.sep + "output.txt"
        error = workdir + os.sep + "error.txt"
        
        job_string = """
#PBS -S /bin/bash
#PBS -N %s
#PBS -l %s
#PBS -l %s
#PBS -l %s
#PBS -o %s
#PBS -e %s
cd %s
%s""" % (job_name, walltime, num_nodes, memory, output, error, workdir,
         command)
        
        return job_string

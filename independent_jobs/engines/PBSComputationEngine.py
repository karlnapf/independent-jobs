
import os
import time

from independent_jobs.engines.BatchClusterComputationEngine import BatchClusterComputationEngine


class PBSComputationEngine(BatchClusterComputationEngine):
    def __init__(self, batch_parameters, check_interval=10, do_clean_up=False):
        BatchClusterComputationEngine.__init__(self,
                                               batch_parameters=batch_parameters,
                                               check_interval=check_interval,
                                               submission_cmd="qsub",
                                               do_clean_up=do_clean_up)

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

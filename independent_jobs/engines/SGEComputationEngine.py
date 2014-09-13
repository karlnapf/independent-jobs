
import os
import time

from independent_jobs.engines.BatchClusterComputationEngine import BatchClusterComputationEngine


class SGEComputationEngine(BatchClusterComputationEngine):
    def __init__(self, batch_parameters, check_interval=10, do_clean_up=False):
        BatchClusterComputationEngine.__init__(self,
                                               batch_parameters=batch_parameters,
                                               check_interval=check_interval,
                                               submission_cmd="qsub",
                                               do_clean_up=do_clean_up)

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

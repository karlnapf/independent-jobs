import os
import popen2

from independent_jobs.engines.BatchClusterComputationEngine import BatchClusterComputationEngine
from independent_jobs.tools.Log import logger
from independent_jobs.tools.Time import Time


class SlurmComputationEngine(BatchClusterComputationEngine):
    def __init__(self, batch_parameters, check_interval=10, do_clean_up=False):
        BatchClusterComputationEngine.__init__(self,
                                               batch_parameters=batch_parameters,
                                               check_interval=check_interval,
                                               submission_cmd="sbatch",
                                               do_clean_up=do_clean_up,
                                               submission_delay=0.01,
                                               max_jobs_in_queue=2000)
        
        # automatically set queue if not specified by user
        try:
            qos = self.batch_parameters.qos
        except AttributeError:
            if self.batch_parameters.max_walltime <= 60 * 60 and \
               self.batch_parameters.nodes <= 90:
                qos = "short"
            elif self.batch_parameters.max_walltime <= 60 * 60 * 24 and \
                 self.batch_parameters.nodes <= 70:
                qos = "normal"
            elif self.batch_parameters.max_walltime <= 60 * 60 * 72 and \
                 self.batch_parameters.nodes <= 20:
                qos = "medium"
            elif self.batch_parameters.max_walltime <= 60 * 60 * 24 and \
                 self.batch_parameters.nodes <= 10:
                qos = "long"
            else:
                logger.info("Unable to infer slurm qos. Setting to normal")
                qos = "normal"
            
            logger.info("Infered slurm qos: %s", qos)
            self.batch_parameters.qos = qos

    def create_batch_script(self, job_name, dispatcher_string):
        command = "nice -n 10 " + dispatcher_string
        
        days, hours, minutes, seconds = Time.sec_to_all(self.batch_parameters.max_walltime)
        walltime = '%d-%d:%d:%d' % (days, hours, minutes, seconds)
        
        num_nodes = str(self.batch_parameters.nodes)
        # note memory is in megabyes
        memory = str(self.batch_parameters.memory)
        workdir = self.get_job_foldername(job_name)
        
        output = workdir + os.sep + "output.txt"
        error = workdir + os.sep + "error.txt"
        
        job_string = """#!/bin/bash
#SBATCH -J %s
#SBATCH --time=%s
#SBATCH --qos=%s
#SBATCH -n %s
#SBATCH --mem=%s
#SBATCH --output=%s
#SBATCH --error=%s
cd %s
%s""" % (job_name, walltime, self.batch_parameters.qos, num_nodes, memory, output, error, workdir,
         command)
        
        return job_string

    def submit_to_batch_system(self, job_string):
        # send job_string to batch command
        outpipe, inpipe = popen2.popen2(self.submission_cmd)
        inpipe.write(job_string + os.linesep)
        inpipe.close()
        
        job_id = outpipe.read().strip().split(" ")[-1]
        outpipe.close()
        
        return job_id
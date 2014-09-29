import glob
import os
import pickle

from independent_jobs.tools.FileSystem import FileSystem
from independent_jobs.tools.Log import logger

def resubmit(job_dir, resubmit_pattern_match, batch_engine):
    dirs = glob.glob(job_dir + "job*")
        
    resubmit = []
    for d in dirs:
        a_fname = d + os.sep + "aggregator.bin"
        j_fname = d + os.sep + "job.bin"
        if not FileSystem.file_exists_new_shell(a_fname):
            with open(j_fname, "r") as f:
                partial_posterior = pickle.load(f).partial_posterior
                if resubmit_pattern_match(partial_posterior):
                    logger.info("%s unfinished" % d.split(os.sep)[-1])
                    resubmit.append(d)
                    
    for d in resubmit:
        with open(d + os.sep + "batch_script", "r") as f:
            job_string = f.readlines()
            
    batch_engine.submit_to_batch_system(job_string)

import os


def resubmit(job_dir, batch_engine):
    if not job_dir[-1] == os.sep:
        job_dir += os.sep
    
    fname = job_dir + "batch_script"
    with open(fname, "r") as f:
        job_string = "".join(f.readlines())
            
    batch_engine.submit_to_batch_system(job_string)

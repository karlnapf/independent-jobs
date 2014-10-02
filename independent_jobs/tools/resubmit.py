def resubmit(job_dir, batch_engine):
    fname = job_dir + "batch_script"
    with open(fname, "r") as f:
        job_string = f.readlines()
            
    batch_engine.submit_to_batch_system(job_string)

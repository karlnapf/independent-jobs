import os
from os.path import expanduser

from independent_jobs.engines.BatchClusterParameters import BatchClusterParameters
from independent_jobs.engines.SerialComputationEngine import SerialComputationEngine
from independent_jobs.jobs.FireAndForgetJob import DummyFireAndForgetJob
from independent_jobs.tools.Log import Log

if __name__ == '__main__':
    """
    Example that just sends out jobs that store their result to a file when done.
    No aggregators are stored and results can be picked up from disc when ready.
    """
    Log.set_loglevel(10)
    # create folder name string
    home = expanduser("~")
    foldername = os.path.join(home, "test")
    db_fname = os.path.join(foldername, "test.txt")
    
    # create parameter instance that is needed for any batch computation engine
    batch_parameters = BatchClusterParameters(foldername=foldername)
    engine = SerialComputationEngine()
    
    for i in range(3):
        for j in range(3):
            job = DummyFireAndForgetJob(db_fname, result_name="score",
                                        i=i, j=j, other="gnaaa")
            engine.submit_job(job)
    
    # optional
    engine.wait_for_all()
    
    

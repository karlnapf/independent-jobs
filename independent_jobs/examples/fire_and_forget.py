import os
from os.path import expanduser

from independent_jobs.engines.BatchClusterParameters import BatchClusterParameters
from independent_jobs.engines.SerialComputationEngine import SerialComputationEngine
from independent_jobs.examples.MyFireAndForgetJob import MyFireAndForgetJob
from independent_jobs.tools.Log import Log


if __name__ == '__main__':
    """
    Example that just sends out jobs that store their result to a file when done;
    there is no control over the job after it has been submitted.
    No aggregators are stored and results can be picked up from disc when ready.
    
    Make sure to read the minimal example first.
    """
    Log.set_loglevel(10)

    # filename of the result database
    home = expanduser("~")
    foldername = os.path.join(home, "test")
    db_fname = os.path.join(foldername, "test.txt")
    
    batch_parameters = BatchClusterParameters(foldername=foldername)
    engine = SerialComputationEngine()
    
    for i in range(3):
        for j in range(3):
            # note there are no aggregators and no result instances
            job = MyFireAndForgetJob(db_fname, result_name="my_result_name",
                                        i=i, j=j, other="some_other_parameter")
            engine.submit_job(job)
    
    

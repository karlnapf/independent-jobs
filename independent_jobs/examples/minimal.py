import os
from os.path import expanduser

from independent_jobs.aggregators.ScalarResultAggregator import ScalarResultAggregator
from independent_jobs.engines.BatchClusterParameters import BatchClusterParameters
from independent_jobs.engines.SGEComputationEngine import SGEComputationEngine
from independent_jobs.engines.SerialComputationEngine import SerialComputationEngine
from independent_jobs.examples.MyJob import MyJob
from independent_jobs.tools.Log import Log
from independent_jobs.tools.Log import logger
import numpy as np


# See other file for implementation of MyJob
# Since we are using ScalarResult, we can use the already implemented aggregator
# ScalarResultAggregator
if __name__ == '__main__':
    Log.set_loglevel(logger.info)
    logger.info("Start")
    # create an instance of the SGE engine, with certain parameters
    
    # create folder name string
    home = expanduser("~")
    foldername = os.sep.join([home, "minimal_example"])
    logger.info("Setting engine folder to %s" % foldername)
    
    # create parameter instance that is needed for any batch computation engine
    logger.info("Creating batch parameter instance")
    batch_parameters = BatchClusterParameters(foldername=foldername)
    
    # possibly create SGE engine instance, which can be used to submit jobs to
    # there are more engines available.
#     logger.info("creating SGE engine instance")
#     engine = SGEComputationEngine(batch_parameters, check_interval=1)
    
#    # create serial engine (which works locally)
    logger.info("Creating serial engine instance")
    engine = SerialComputationEngine()
    
    # we have to collect aggregators somehow
    aggregators = []
    
    # submit job three times
    logger.info("Starting loop over job submission")
    for i in range(3):
        logger.info("Submitting job %d" % i)
        job = MyJob(ScalarResultAggregator())
        aggregators.append(engine.submit_job(job))
        
    # let the engine finish its business
    logger.info("Wait for all call in engine")
    engine.wait_for_all()
    
    # lets collect the results
    results = np.zeros(len(aggregators))
    logger.info("Collecting results")
    for i in range(len(aggregators)):
        logger.info("Collecting result %d" % i)
        # let the aggregator finalize things, not really needed here but in general
        aggregators[i].finalize()
        
        # aggregators[i].get_final_result() returns a ScalarResult instance,
        # which we need to extract the number from
        results[i] = aggregators[i].get_final_result().result
    
    print "Results", results

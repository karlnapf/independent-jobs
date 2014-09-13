

import logging
from numpy.ma.core import zeros
import os
from os.path import expanduser

from independent_jobs.aggregators.ScalarResultAggregator import ScalarResultAggregator
from independent_jobs.engines.BatchClusterParameters import BatchClusterParameters
from independent_jobs.engines.SGEComputationEngine import SGEComputationEngine
from independent_jobs.engines.SerialComputationEngine import SerialComputationEngine
from independent_jobs.examples.MyJob import MyJob
from independent_jobs.tools.Log import Log


# See other file for implementation of MyJob
# Since we are using ScalarResult, we can use the already implemented aggregator
# ScalarResultAggregator
if __name__ == '__main__':
    Log.set_loglevel(logging.INFO)
    logging.info("Start")
    # create an instance of the SGE engine, with certain parameters
    
    # create folder name string
    home = expanduser("~")
    foldername = os.sep.join([home, "minimal_example"])
    logging.info("Setting engine folder to %s" % foldername)
    
    # create parameter instance that is needed for any batch computation engine
    logging.info("Creating batch parameter instance")
    batch_parameters = BatchClusterParameters(foldername=foldername)
    
    # possibly create SGE engine instance, which can be used to submit jobs to
    # there are more engines available.
#     logging.info("creating SGE engine instance")
#     engine = SGEComputationEngine(batch_parameters, check_interval=1)
    
#    # create serial engine (which works locally)
    logging.info("Creating serial engine instance")
    engine = SerialComputationEngine()
    
    # we have to collect aggregators somehow
    aggregators = []
    
    # submit job three times
    logging.info("Starting loop over job submission")
    for i in range(3):
        logging.info("Submitting job %d" % i)
        job = MyJob(ScalarResultAggregator())
        aggregators.append(engine.submit_job(job))
        
    # let the engine finish its business
    logging.info("Wait for all call in engine")
    engine.wait_for_all()
    
    # lets collect the results
    results = zeros(len(aggregators))
    logging.info("Collecting results")
    for i in range(len(aggregators)):
        logging.info("Collecting result %d" % i)
        # let the aggregator finalize things, not really needed here but in general
        aggregators[i].finalize()
        
        # aggregators[i].get_final_result() returns a ScalarResult instance,
        # which we need to extract the number from
        results[i] = aggregators[i].get_final_result().result
    
    print "Results", results

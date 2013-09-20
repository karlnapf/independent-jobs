from aggregators.ScalarResultAggregator import ScalarResultAggregator
from engines.BatchClusterParameters import BatchClusterParameters
from engines.SGEComputationEngine import SGEComputationEngine
from engines.SerialComputationEngine import SerialComputationEngine
from jobs.IndependentJob import IndependentJob
from numpy.ma.core import zeros
from os.path import expanduser
from results.ScalarResult import ScalarResult
from time import sleep
from tools.Log import Log
import logging
import os

# Define our custom Job, which inherits from base class IndependentJob
class MyJob(IndependentJob):
    def __init__(self, aggregator):
        IndependentJob.__init__(self, aggregator)
    
    # we need to define the abstract compute method. It has to return an instance
    # of JobResult base class
    def compute(self):
        logging.info("computing")
        # job is to sleep for some time and return this time as an instance
        # of ScalarResult, which is a provided sub-class of JobResult
        sleep_time = 3
        
        sleep(sleep_time)
        
        # create ScalarResult instance
        result = ScalarResult(sleep_time)
        
        # submit the result to my own aggregator
        self.aggregator.submit_result(result)
    
    
# Since we are using ScalarResult, we can use the already implemented aggregator
# ScalarResultAggregator


if __name__ == '__main__':
    Log.set_loglevel(logging.INFO)
    logging.info("start")
    # create an instance of the SGE engine, with certain parameters
    
    # create folder name string
    home = expanduser("~")
    foldername = os.sep.join([home, "minimal_example_sge"])
    logging.info("setting engine folder to %s" % foldername)
    
    # create parameter instance that is needed for any batch computation engine
    logging.info("creating batch parameter instance")
    batch_parameters = BatchClusterParameters(foldername=foldername)
    
    # finally, create SGE engine instance, which can be used to submit jobs to
    logging.info("creating SGE engine instance")
    engine = SGEComputationEngine(batch_parameters, check_interval=1)
    
#    # replace engine by serial engine (which is already implemented) to test things
#    logging.info("Replacing engine with serial engine instance")
#    engine = SerialComputationEngine()
    
    # we have to collect aggregators somehow
    aggregators = []
    
    # submit job three times
    logging.info("starting loop over job submission")
    for i in range(3):
        logging.info("submitting job %d" % i)
        job = MyJob(ScalarResultAggregator())
        aggregators.append(engine.submit_job(job))
        
    # let the engine finish its business
    logging.info("wait for all call in engine")
    engine.wait_for_all()
    
    # lets collect the results
    results = zeros(len(aggregators))
    logging.info("Collecting results")
    for i in range(len(aggregators)):
        logging.info("collecting result %d" % i)
        # let the aggregator finalize things, not really needed here but in general
        aggregators[i].finalize()
        
        # aggregators[i].get_final_result() returns a ScalarResult instance,
        # which we need to extract the number from
        results[i] = aggregators[i].get_final_result().result
    
    print "results", results

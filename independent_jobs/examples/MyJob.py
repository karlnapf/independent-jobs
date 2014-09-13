
import logging
from numpy.random import randint
from time import sleep

from independent_jobs.jobs.IndependentJob import IndependentJob
from independent_jobs.results.ScalarResult import ScalarResult


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
        sleep_time = randint(10)
        
        logging.info("sleeping for %d seconds" % sleep_time)
        sleep(sleep_time)
        
        # create ScalarResult instance
        result = ScalarResult(sleep_time)
        
        # submit the result to my own aggregator
        self.aggregator.submit_result(result)
        logging.info("done computing")
        

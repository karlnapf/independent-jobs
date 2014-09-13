
import logging
from numpy.random import randint
from time import sleep

from independent_jobs.jobs.IndependentJob import IndependentJob
from independent_jobs.results.ScalarResult import ScalarResult


class DummyJob(IndependentJob):
    def __init__(self, aggregator, sleep_time):
        IndependentJob.__init__(self, aggregator)
        self.sleep_time = sleep_time
    
    def compute(self):
        result = ScalarResult(self.sleep_time)
        
        if self.sleep_time >= 0:
            sleep_time = self.sleep_time
        else:
            sleep_time = randint(10)
            
        logging.info("Sleeping for %d" % sleep_time)
        sleep(sleep_time)
            
        self.aggregator.submit_result(result)

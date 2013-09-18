"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from jobs.IndependentJob import IndependentJob
from numpy.random import randint
from results.ScalarResult import ScalarResult
from time import sleep
import logging

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

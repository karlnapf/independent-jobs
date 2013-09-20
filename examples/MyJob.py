"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from jobs.IndependentJob import IndependentJob
from results.ScalarResult import ScalarResult
import logging
from time import sleep

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
"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from engines.IndependentComputationEngine import IndependentComputationEngine

class SerialComputationEngine(IndependentComputationEngine):
    def __init__(self):
        IndependentComputationEngine.__init__(self)
    
    def submit_job(self, job):
        job.compute()
        return job.aggregator
    
    def wait_for_all(self):
        pass

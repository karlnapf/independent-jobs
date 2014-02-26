"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from aggregators.JobResultAggregator import JobResultAggregator

class ScalarResultAggregator(JobResultAggregator):
    def __init__(self):
        JobResultAggregator.__init__(self, 1)
    
    def finalize(self):
        pass
    
    def submit_result(self, result):
        self.result = result
    
    def get_final_result(self):
        return self.result
    
    def clean_up(self):
        pass


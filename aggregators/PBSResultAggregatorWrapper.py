"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from aggregators.JobResultAggregator import JobResultAggregator
from pickle import dump, load

class PBSResultAggregatorWrapper(JobResultAggregator):
    def __init__(self, wrapped_aggregator, filename):
        self.wrapped_aggregator = wrapped_aggregator
        self.filename = filename
        
        # to keep track of all submitted results
        self.result_counter = 0
    
    def submit_result(self, result):
        # NOTE: this happens on the PBS

        # pass on result to wrapper wrapped_aggregator
        self.wrapped_aggregator.submit_result(result)
        self.result_counter += 1
        
        # if all results received, dump wrapped_aggregator to disc
        # this has to happen on the PBS
        if self.result_counter == self.wrapped_aggregator.expected_num_results:
            f = open(self.filename, 'w')
            dump(self.wrapped_aggregator, f)
            f.close()
        
    def finalize(self):
        # NOTE: This happens in the PBS engine, so not on the PBS
        
        # load the previously dumped aggregator to this instance, which is empty
        # since the filled one is on the PBS
        f = open(self.filename, 'r')
        self.wrapped_aggregator = load(f)
        f.close()
    
    def get_final_result(self):
        # NOTE: This happens in the PBS engine, so not on the PBS
        
        # return previously loaded finalised result
        return self.wrapped_aggregator.get_final_result()

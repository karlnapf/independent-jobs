"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from aggregators.ScalarResultAggregator import ScalarResultAggregator
from engines.PBSComputationEngine import PBSComputationEngine
from jobs.DummyJob import DummyJob
from jobs.BatchClusterParameters import BatchClusterParameters
from numpy.random import randint
from os.path import expanduser
import os
import shutil
import unittest

class DummyComputation(object):
    def __init__(self, engine):
        self.engine = engine
    
    def go_to_bed(self, sleep_time):
        job = DummyJob(ScalarResultAggregator(), sleep_time)
        agg = self.engine.submit_job(job)
        return agg

class DummyJobTests(unittest.TestCase):
    def engine_tester(self, engine, sleep_times):
        dc = DummyComputation(engine)
        
        aggregators = []
        num_submissions = len(sleep_times)
        for i in range(num_submissions):
            aggregators.append(dc.go_to_bed(sleep_times[i]))
            
        self.assertEqual(len(aggregators), num_submissions)
        
        engine.wait_for_all()
        
        results = []
        for i in range(num_submissions):
            aggregators[i].finalize()
            results.append(aggregators[i].get_final_result().result)
            
        for i in range(num_submissions):
            self.assertEqual(results[i], sleep_times[i])

    def test_pbs_engine_max_waiting_time(self):
        home = expanduser("~")
        folder = os.sep.join([home, "unit_test_dummy_pbs_result_max_wait"])
        
        try:
            shutil.rmtree(folder)
        except OSError:
            pass
        batch_parameters = BatchClusterParameters(foldername=folder, max_walltime=8)
        engine = PBSComputationEngine(batch_parameters, check_interval=1)
        sleep_times = [2, -1]
        self.engine_tester(engine, sleep_times)
        
    def test_pbs_engine(self):
        home = expanduser("~")
        folder = os.sep.join([home, "unit_test_pbs_dummy_result"])
        try:
            shutil.rmtree(folder)
        except OSError:
            pass
        batch_parameters = BatchClusterParameters(foldername=folder)
        engine = PBSComputationEngine(batch_parameters, check_interval=1)
        num_submissions = 3
        sleep_times = randint(0, 3, num_submissions)
        self.engine_tester(engine, sleep_times)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

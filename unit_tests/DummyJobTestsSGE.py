"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from aggregators.ScalarResultAggregator import ScalarResultAggregator
from engines.SGEComputationEngine import SGEComputationEngine
from jobs.DummyJob import DummyJob
from jobs.PBSParameters import PBSParameters
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

    def test_sge_engine(self):
        home = expanduser("~")
        folder = os.sep.join([home, "unit_test_sge_dummy_result"])
        try:
            shutil.rmtree(folder)
        except OSError:
            pass
        pbs_parameters = PBSParameters(foldername=folder)
        engine = SGEComputationEngine(pbs_parameters, check_interval=1)
        num_submissions = 3
        sleep_times = randint(0, 3, num_submissions)
        self.engine_tester(engine, sleep_times)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

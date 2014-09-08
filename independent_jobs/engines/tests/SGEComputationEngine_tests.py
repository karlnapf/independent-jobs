"""
Copyright (c) 2013-2014 Heiko Strathmann
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 *
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 *
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the author.
"""
from nose import SkipTest
from numpy.random import randint
import os
from os.path import expanduser
import shutil
import unittest

from independent_jobs.aggregators.ScalarResultAggregator import ScalarResultAggregator
from independent_jobs.engines.BatchClusterParameters import BatchClusterParameters
from independent_jobs.engines.SGEComputationEngine import SGEComputationEngine
from independent_jobs.jobs.DummyJob import DummyJob
from independent_jobs.tools.FileSystem import FileSystem

class DummyComputation(object):
    def __init__(self, engine):
        self.engine = engine
    
    def go_to_bed(self, sleep_time):
        job = DummyJob(ScalarResultAggregator(), sleep_time)
        agg = self.engine.submit_job(job)
        return agg

class DummyJobTests(unittest.TestCase):
    def engine_helper(self, engine, sleep_times):
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
            aggregators[i].clean_up()
            
        for i in range(num_submissions):
            self.assertEqual(results[i], sleep_times[i])
        
        if engine.do_clean_up:
            for i in range(num_submissions):
                self.assertFalse(FileSystem.file_exists_new_shell(aggregators[i].filename))

    def test_sge_engine(self):
        if not FileSystem.cmd_exists("qsub"):
            raise SkipTest

        home = expanduser("~")
        folder = os.sep.join([home, "unit_test_sge_dummy_result"])
        try:
            shutil.rmtree(folder)
        except OSError:
            pass
        batch_parameters = BatchClusterParameters(foldername=folder)
        engine = SGEComputationEngine(batch_parameters, check_interval=1)
        num_submissions = 3
        sleep_times = randint(0, 3, num_submissions)
        self.engine_helper(engine, sleep_times)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

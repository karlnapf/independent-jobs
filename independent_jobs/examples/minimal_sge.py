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

import logging
from numpy.ma.core import zeros
import os
from os.path import expanduser

from independent_jobs.aggregators.ScalarResultAggregator import ScalarResultAggregator
from independent_jobs.engines.BatchClusterParameters import BatchClusterParameters
from independent_jobs.engines.SGEComputationEngine import SGEComputationEngine
from independent_jobs.engines.SerialComputationEngine import SerialComputationEngine
from independent_jobs.examples.MyJob import MyJob
from independent_jobs.tools.Log import Log


# See other file for implementation of MyJob
# Since we are using ScalarResult, we can use the already implemented aggregator
# ScalarResultAggregator
if __name__ == '__main__':
    Log.set_loglevel(logging.INFO)
    logging.info("start")
    # create an instance of the SGE engine, with certain parameters
    
    # create folder name string
    home = expanduser("~")
    foldername = os.sep.join([home, "minimal_example_sge"])
    logging.info("setting engine folder to %s" % foldername)
    
    # create parameter instance that is needed for any batch computation engine
    logging.info("creating batch parameter instance")
    batch_parameters = BatchClusterParameters(foldername=foldername)
    
    # finally, create SGE engine instance, which can be used to submit jobs to
    logging.info("creating SGE engine instance")
    engine = SGEComputationEngine(batch_parameters, check_interval=1)
    
#    # replace engine by serial engine (which is already implemented) to test things
#    logging.info("Replacing engine with serial engine instance")
#    engine = SerialComputationEngine()
    
    # we have to collect aggregators somehow
    aggregators = []
    
    # submit job three times
    logging.info("starting loop over job submission")
    for i in range(3):
        logging.info("submitting job %d" % i)
        job = MyJob(ScalarResultAggregator())
        aggregators.append(engine.submit_job(job))
        
    # let the engine finish its business
    logging.info("wait for all call in engine")
    engine.wait_for_all()
    
    # lets collect the results
    results = zeros(len(aggregators))
    logging.info("Collecting results")
    for i in range(len(aggregators)):
        logging.info("collecting result %d" % i)
        # let the aggregator finalize things, not really needed here but in general
        aggregators[i].finalize()
        
        # aggregators[i].get_final_result() returns a ScalarResult instance,
        # which we need to extract the number from
        results[i] = aggregators[i].get_final_result().result
    
    print "results", results

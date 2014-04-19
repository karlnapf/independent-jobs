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
import os
from pickle import dump, load

from aggregators.JobResultAggregator import JobResultAggregator
from tools.FileSystem import FileSystem


class PBSResultAggregatorWrapper(JobResultAggregator):
    def __init__(self, wrapped_aggregator, filename, job_name, do_clean_up = False):
        self.wrapped_aggregator = wrapped_aggregator
        self.filename = filename
        self.job_name = job_name
        
        # to keep track of all submitted results
        self.result_counter = 0
        
        # whether to delete job output
        self.do_clean_up = do_clean_up
    
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

    def clean_up(self):
        if self.do_clean_up:
            FileSystem.delete_dir_failsafe(os.sep.join(self.filename.split(os.sep)[:-1]))
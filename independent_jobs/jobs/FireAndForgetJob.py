import numpy as np
import os
import time

from independent_jobs.aggregators.SingleResultAggregator import SingleResultAggregator
from independent_jobs.jobs.IndependentJob import IndependentJob
from independent_jobs.tools.Log import logger

import pandas as pd
from abc import abstractmethod

def store_results(fname=os.path.expanduser("~") + os.sep + "results.txt", **kwargs):
    # add filename if only path is given
    if fname[-1] == os.sep:
        fname += "results.txt"
    
    # create result dir if wanted
    if os.sep in fname:
        try:
            directory = os.sep.join(fname.split(os.sep)[:-1])
            os.makedirs(directory)
        except OSError:
            pass
    
    # use current time as index for the dataframe
    current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())
    new_df = pd.DataFrame([[kwargs[k] for k in kwargs.keys()]], index=[current_time], columns=kwargs.keys())
    
    if os.path.exists(fname):
        df = pd.read_csv(fname, index_col=0)
        df = df.append(new_df)
    else:
        df = new_df

    # very crude protection against conflicting access from parallel processes
    write_success = False
    while not write_success:
        try:
            df.to_csv(fname)
            write_success = True
        except IOError:
            print("IOError writing to csv ... trying again in 1s.")
            time.sleep(1)


class FireAndForgetJob(IndependentJob):
    def __init__(self, db_fname, result_name="result", **param_dict):
        IndependentJob.__init__(self, SingleResultAggregator())
        
        self.db_fname = db_fname
        self.param_dict = param_dict
        self.result_name = result_name
    
    @abstractmethod
    def compute_result(self):
        raise NotImplementedError()
    
    def compute(self):
        param_string = ",".join(["%s=%s" % (str(k), str(v)) for k, v in self.param_dict.items()])
        logger.info("Computing result for %s" % param_string)
        result = self.compute_result()
        self.store_results(result)
    
    def store_results(self, result):
        logger.info("Storing results in %s" % self.db_fname)
        submit_dict = {}
        for k, v in self.param_dict.items():
            submit_dict[k] = v
        submit_dict[self.result_name] = result
        store_results(self.db_fname, **submit_dict)

class DummyFireAndForgetJob(FireAndForgetJob):
    def __init__(self, db_fname, result_name="result", **param_dict):
        FireAndForgetJob.__init__(self, db_fname, result_name, **param_dict)
    
    @abstractmethod
    def compute_result(self):
        return np.random.randn()

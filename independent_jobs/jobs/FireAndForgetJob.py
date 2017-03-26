from abc import abstractmethod
import os
import time
import itertools

from independent_jobs.aggregators.ScalarResultAggregator import ScalarResultAggregator
from independent_jobs.aggregators.SingleResultAggregator import SingleResultAggregator
from independent_jobs.jobs.IndependentJob import IndependentJob
from independent_jobs.tools.Log import logger
import numpy as np
import pandas as pd


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
            sleep_time = np.random.randint(5)
            print("IOError writing to csv ... trying again in %d." % sleep_time)
            time.sleep(1)

def extract_array(fname, param_names, result_name="result",
                  non_existing=np.nan, redux_funs=[np.mean], return_param_values=True,
                  conditionals={}):
    """
    Given a csv file (as e.g. product by FireAndForgetJob, extraxts an
    array where each dimension corresponds to a provided parameter, and
    each element is a redux (e.g. mean) of all results (of given same)
    for the parameter combinations.
    An optional set of additional conditions can be specified.
    
    A default value can be specified.
    """
    with open(fname) as f:
        df = pd.read_csv(f)
    
    param_values = {}
    for param in param_names:
        values = np.sort(np.unique(df[param]))
        values = values[~np.isnan(values)]
        param_values[param] = values
    
    sizes = [len(param_values[param]) for param in param_names]
    results = [np.zeros(tuple(sizes)) + non_existing for _ in redux_funs]
    
    all_combs = itertools.product(*[param_values[param] for param in param_names])
    
    for comb in all_combs:
        masks = [df[param] == comb[i] for i, param in enumerate(param_names)]
        masks += [df[k]==v for k,v in conditionals.items()]
        
        lines = df
        for mask in masks:
            lines = lines[mask]
        
        if len(lines) > 0:
            for j, redux_fun in enumerate(redux_funs):
                result = redux_fun(lines[result_name].values)
                ind_array = tuple([np.where(param_values[param] == comb[i])[0][0] for i, param in enumerate(param_names)])
                results[j][ind_array] = result

    if not return_param_values:
        return results
    else:
        return results, param_values

def best_parameters(db_fname, param_names, result_name, selector=np.nanmin,
                    redux_fun=np.nanmean, plot=False, conditionals={}):
    """
    Extracts the best choice of parameters using @see extract_array
    """
    results, param_values = extract_array(db_fname,
                            result_name=result_name,
                            param_names=param_names,
                            redux_funs=[redux_fun],
                            conditionals=conditionals)
    
    results = results[0]

    best_ind = np.unravel_index(np.nanargmin(results), results.shape)

    best_params = {}
    for i, param_name in enumerate(param_names):
        best_params[param_name] = param_values[param_name][best_ind[i]]
    
    return best_params, selector(results)

class FireAndForgetJob(IndependentJob):
    def __init__(self, db_fname, result_name="result", **param_dict):
        IndependentJob.__init__(self, ScalarResultAggregator())
        
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
        self.aggregator.submit_result(result)
    
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

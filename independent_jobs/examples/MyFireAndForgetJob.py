from abc import abstractmethod
from time import sleep

from independent_jobs.jobs.FireAndForgetJob import FireAndForgetJob
from independent_jobs.tools.Log import logger
import numpy as np


class MyFireAndForgetJob(FireAndForgetJob):
    """
    Minimal fire and forget job that returns a random number after a random delay
    """
    def __init__(self, db_fname, result_name="result", **param_dict):
        FireAndForgetJob.__init__(self, db_fname, result_name, **param_dict)
    
    @abstractmethod
    def compute_result(self):
        """
        Note that this method directly computes and returns the result itself.
        There is no aggregators and no result instances being passed around at
        this point.
        """
        sleep_time = np.random.randint(10)
        logger.info("sleeping for %d seconds" % sleep_time)
        sleep(sleep_time)

        return sleep_time
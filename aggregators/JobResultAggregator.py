"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from abc import abstractmethod


class JobResultAggregator(object):
    def __init__(self, expected_num_results):
        self.expected_num_results = expected_num_results
    
    @abstractmethod
    def finalize(self):
        raise NotImplementedError()
    
    @abstractmethod
    def submit_result(self, result):
        raise NotImplementedError()
    
    @abstractmethod
    def get_final_result(self):
        raise NotImplementedError()
    
    @abstractmethod
    def clean_up(self):
        raise NotImplementedError()


"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from abc import abstractmethod

class IndependentJob(object):
    def __init__(self, aggregator):
        self.aggregator = aggregator
    
    @abstractmethod
    def compute(self):
        raise NotImplementedError()

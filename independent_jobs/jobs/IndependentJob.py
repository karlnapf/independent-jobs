
from abc import abstractmethod

class IndependentJob(object):
    def __init__(self, aggregator):
        self.aggregator = aggregator
    
    @abstractmethod
    def compute(self):
        raise NotImplementedError()

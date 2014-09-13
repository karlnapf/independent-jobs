
import logging

class BatchClusterParameters(object):
    def __init__(self, foldername="", job_name_base="job_", \
                 max_walltime=3600, nodes=1, memory=2, loglevel=logging.INFO,
                 parameter_prefix=""):
        self.foldername = foldername
        self.job_name_base = job_name_base
        self.max_walltime = max_walltime
        self.nodes = nodes
        self.memory = memory
        self.loglevel = loglevel
        self.parameter_prefix = parameter_prefix

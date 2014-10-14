import logging
from tempfile import mkdtemp

from independent_jobs.tools.Log import logger


class BatchClusterParameters(object):
    def __init__(self, foldername=None, job_name_base="job_", \
                 max_walltime=3600, nodes=1, memory=2, loglevel=logging.INFO,
                 parameter_prefix="", parameter_suffix="",
                 resubmit_on_timeout=True):
        
        if foldername is None:
            foldername = mkdtemp()
            logger.debug("Creating temp directory for batch job: %s" % foldername)

        self.foldername = foldername
        self.job_name_base = job_name_base
        self.max_walltime = max_walltime
        self.nodes = nodes
        self.memory = memory
        self.loglevel = loglevel
        self.parameter_prefix = parameter_prefix
        self.parameter_suffix = parameter_suffix
        self.resubmit_on_timeout = resubmit_on_timeout

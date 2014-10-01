from abc import abstractmethod
from os import makedirs
import os
from popen2 import popen2
import time

from independent_jobs.aggregators.PBSResultAggregatorWrapper import PBSResultAggregatorWrapper
from independent_jobs.engines.IndependentComputationEngine import IndependentComputationEngine
from independent_jobs.tools.FileSystem import FileSystem
from independent_jobs.tools.Log import logger
from independent_jobs.tools.Serialization import Serialization


class Dispatcher(object):
    @staticmethod
    def dispatch(filename):
        # wait until FS says that the file exists
        while not FileSystem.file_exists_new_shell(filename):
            time.sleep(1)
        
        job = Serialization.deserialize_object(filename)
        job.compute()

class BatchClusterComputationEngine(IndependentComputationEngine):
    def __init__(self, batch_parameters, submission_cmd,
                 check_interval=10, do_clean_up=False, submission_delay=0.5,
                 max_jobs_in_queue=0):
        IndependentComputationEngine.__init__(self)
        
        self.batch_parameters = batch_parameters
        self.check_interval = check_interval
        self.do_clean_up = do_clean_up
        self.submission_cmd = submission_cmd
        self.submission_delay = submission_delay
        self.max_jobs_in_queue = max_jobs_in_queue
        # make sure submission command executable is in path
        if not FileSystem.cmd_exists(submission_cmd):
            raise ValueError("Submission command executable \"%s\" not found" % submission_cmd)
        
        # list of tuples of (job_name, submission_time), which is kept in sorted
        # order by the time
        self.submitted_jobs = []
    
    def get_aggregator_filename(self, job_name):
        job_folder = self.get_job_foldername(job_name)
        return os.sep.join([job_folder, "aggregator.bin"])
    
    def get_job_foldername(self, job_name):
        return os.sep.join([self.batch_parameters.foldername, job_name])
    
    def get_job_filename(self, job_name):
        return os.sep.join([self.get_job_foldername(job_name), "job.bin"])
    
    @abstractmethod
    def create_batch_script(self, job_name, dispatcher_string):
        raise NotImplementedError()
    
    def _get_num_unfinished_jobs(self):
        return len(self.submitted_jobs)
    
    def _insert_job_time_sorted(self, job_name):
        self.submitted_jobs.append((job_name, time.time()))
        
        # sort list by second element (in place)
        self.submitted_jobs.sort(key=lambda tup: tup[1])
    
    def _get_oldest_job_in_queue(self):
        return self.submitted_jobs[0][0] if len(self.submitted_jobs) > 0 else None
    
    def submit_wrapped_pbs_job(self, wrapped_job, job_name):
        job_folder = self.get_job_foldername(job_name)
        
        # track submitted (and unfinished) jobs and their start time
        self._insert_job_time_sorted(job_name)
        
        # try to create folder if not yet exists
        job_filename = self.get_job_filename(job_name)
        logger.info("Creating job with file %s" % job_filename)
        try:
            makedirs(job_folder)
        except OSError:
            pass
        
        Serialization.serialize_object(wrapped_job, job_filename)
        
        # allow the queue to process things        
        time.sleep(self.submission_delay)
        
        lines = []
        lines.append("from independent_jobs.engines.BatchClusterComputationEngine import Dispatcher")
        lines.append("from independent_jobs.tools.Log import Log")
        lines.append("Log.set_loglevel(%d)" % self.batch_parameters.loglevel)
        lines.append("filename=\"%s\"" % job_filename)
        lines.append("Dispatcher.dispatch(filename)")
        
        dispatcher_string = "python -c '" + os.linesep.join(lines) + "'"
        
        job_string = self.create_batch_script(job_name, dispatcher_string)
        
        # put the custom parameter string in front if existing
        if self.batch_parameters.parameter_prefix != "":
            job_string = os.linesep.join([self.batch_parameters.parameter_prefix,
                                         job_string])
        
        f = open(job_folder + os.sep + "batch_script", "w")
        f.write(job_string)
        f.close()
        
        job_id = self.submit_to_batch_system(job_string)
        
        if job_id == "":
            raise RuntimeError("Could not parse job_id. Something went wrong with the job submission")
        
        f = open(job_folder + os.sep + "job_id", 'w')
        f.write(job_id + os.linesep)
        f.close()
    
    def submit_to_batch_system(self, job_string):
        # send job_string to batch command
        outpipe, inpipe = popen2(self.submission_cmd)
        inpipe.write(job_string + os.linesep)
        inpipe.close()
        
        job_id = outpipe.read().strip()
        outpipe.close()
        
        return job_id
    
    def create_job_name(self):
        return FileSystem.get_unique_filename(self.batch_parameters.job_name_base)
    
    def submit_job(self, job):
        # first step: check how many jobs are there in the queue, and if we
        # should wait for submission until this has dropped under a certain value
        if self.max_jobs_in_queue > 0 and \
           self._get_num_unfinished_jobs() >= self.max_jobs_in_queue:
            logger.info("Reached maximum number of %d unfinished jobs in queue." % 
                        self.max_jobs_in_queue)
            self._wait_until_n_unfinished(self.max_jobs_in_queue)
        
        
        # replace job's wrapped_aggregator by PBS wrapped_aggregator to allow
        # FS based communication
        
        # use a unique job name, but check that this folder doesnt yet exist
        job_name = self.create_job_name()
        
        aggregator_filename = self.get_aggregator_filename(job_name)
        job.aggregator = PBSResultAggregatorWrapper(job.aggregator,
                                                    aggregator_filename,
                                                    job_name,
                                                    self.do_clean_up)
        
        self.submit_wrapped_pbs_job(job, job_name)
        
        return job.aggregator
    
    def _check_job_done(self, job_name):
        # race condition is fine here, but use a new python shell
        # due to NFS cache problems otherwise
        filename = self.get_aggregator_filename(job_name)
        return FileSystem.file_exists_new_shell(filename)
    
    def _get_max_wait_time_exceed_jobs(self, job_name):
        names = []
        current_time = time.time()
        for job_name, job_time in self.submitted_jobs:
            if abs(current_time - job_time) > self.batch_parameters.max_walltime:
                names += [job_name]
        return names
    
    def _rebsubmit(self, job_name):
        new_job_name = self.create_job_name()
        logger.info("Re-submitting under name %s" % new_job_name)
        
        # remove from submitted list
        self.submitted_jobs.remove(job_name)
        
        # load job from disc and re-submit under new name
        job_filename = self.get_job_filename(job_name)
        wrapped_job = Serialization.deserialize_object(job_filename)
        self.submit_wrapped_pbs_job(wrapped_job, new_job_name)
        self._insert_job_time_sorted(new_job_name)
    
    def _wait_until_n_unfinished(self, desired_num_unfinished):
        """
        Iteratively checks all non-finished jobs and updates whether they are
        finished. Blocks until there are less or exactly desired_num_unfinished
        unfinished jobs in the queue. Messages a "waiting for" info message
        for the oldest job in the queue.
        """
        
        last_printed = self._get_oldest_job_in_queue()
        logger.info("Waiting for %s and %d other jobs" % (last_printed,
                                                          self._get_num_unfinished_jobs() - 1))
        while self._get_num_unfinished_jobs() > desired_num_unfinished:
            oldest = self._get_oldest_job_in_queue()
            if oldest != last_printed:
                last_printed = oldest
                logger.info("Waiting for %s and %d other jobs" % (last_printed,
                                                                  self._get_num_unfinished_jobs() - 1))
            
            # delete all finished jobs from internal list
            i = 0
            while i < len(self.submitted_jobs):
                job_name = self.submitted_jobs[i][0]
                if self._check_job_done(job_name):
                    del self.submitted_jobs[i]
                    # dont change i as it is now the index of the next element
                else:
                    i += 1
                        
            # check for re-submissions
            if self.batch_parameters.resubmit_on_timeout:
                for job_name in self._get_max_wait_time_exceed_jobs():
                    logger.info("%s exceeded maximum waiting time of %d" 
                                % (job_name, self.batch_parameters.max_walltime))
                    self._resubmit(job_name)
                    
            time.sleep(self.check_interval)

    def wait_for_all(self):
        self._wait_until_n_unfinished(0)
        logger.info("All jobs finished.")

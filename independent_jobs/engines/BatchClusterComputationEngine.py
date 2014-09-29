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
        
        self.submitted_job_map = {}
        self.submitted_job_counter = 0
    
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
    
    def get_num_unfinished_jobs(self):
        return sum([v==False for v in self.submitted_job_map.values()])
    
    def submit_wrapped_pbs_job(self, wrapped_job, job_name):
        job_folder = self.get_job_foldername(job_name)
        
        # track submitted jobs/aggregators for retrieving results from FS later
        # dont do this in memory as it might blow up things
        self.submitted_job_map[job_name] = False
        self.submitted_job_counter += 1
        
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
        
        # send job_string to batch command
        outpipe, inpipe = popen2(self.submission_cmd)
        inpipe.write(job_string + os.linesep)
        inpipe.close()
        
        job_id = outpipe.read().strip()
        outpipe.close()
        
        if job_id == "":
            raise RuntimeError("Could not parse job_id. Something went wrong with the job submission")
        
        f = open(job_folder + os.sep + "job_id", 'w')
        f.write(job_id + os.linesep)
        f.close()
    
    def create_job_name(self):
        return FileSystem.get_unique_filename(self.batch_parameters.job_name_base)
    
    def submit_job(self, job):
        # first step: check how many jobs are there in the queue, and if we
        # should wait for submission until this has dropped under a certain value
        if self.max_jobs_in_queue > 0 and \
           self.get_num_unfinished_jobs() > self.max_jobs_in_queue:
            logger.info("Reached maximum number of unfinished jobs (%d) in queue, waiting." %
                        self.max_jobs_in_queue)
            self.wait_for_all(self.max_jobs_in_queue)
        
        
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
    
    def wait_for_all(self, desired_num_unfinished_jobs=0):
        """
        Waits for the number of unfinished jobs reach a given value (usually 0),
        which means that until all result files of all submitted jobs exist.
        Afterwards, the job list is emptied for another trial.
        """
        # check whether there are unfinished jobs
        waiting_start = time.time()
        
        # outer loop is to handle re-submitted jobs
        while self.get_num_unfinished_jobs() > desired_num_unfinished_jobs:
            # iterate over all jobs in list and check whether they are done yet
            for job_name, job_finished in self.submitted_job_map.iteritems():
                filename = self.get_aggregator_filename(job_name)
                
                # do not wait again for finished jobs
                if not job_finished:
                    logger.info("waiting for %s" % job_name)
                
                    # wait until file exists (dangerous, so have a maximum waiting time
                    # after which old job is discarded and replacement is submitted)
                    while self.submitted_job_map[job_name]:
                        # loop over all submitted jobs to update the list of 
                        # unfinished jobs, in this loop however, we use only
                        # the current job_name
                        for job_name in self.submitted_job_map.keys():
                            # race condition is fine here, but use a new python shell
                            # due to NFS cache problems otherwise
                            if FileSystem.file_exists_new_shell(filename):
                                self.submitted_job_map[job_name] = True
                        
                        time.sleep(self.check_interval)
                        
                        # check whether maximum waiting time is over and re-submit if is
                        waited_for = time.time() - waiting_start
                        if self.batch_parameters.resubmit_on_timeout and \
                           waited_for > self.batch_parameters.max_walltime:
                            new_job_name = self.create_job_name()
                            logger.info("%s exceeded maximum waiting time of %d" 
                                        % (job_name, self.batch_parameters.max_walltime))
                            logger.info("Re-submitting under name %s" % new_job_name)
    
                            # remove from submitted list to not wait anymore and
                            # change job name
                            del self.submitted_job_map[job_name]
                            job_filename = self.get_job_filename(job_name)
                            
                            # load job from disc and re-submit
                            wrapped_job = Serialization.deserialize_object(job_filename)
                            self.submit_wrapped_pbs_job(wrapped_job, new_job_name)
                            waiting_start = time.time()
                            
                            # submitted job map has changed, break inner
                            # infinite loop and start again
                            break
                
                # break waiting early if desired number of unfinished jobs reached
                if self.get_num_unfinished_jobs() <= desired_num_unfinished_jobs:
                    break
        
        if self.get_num_unfinished_jobs() == 0:
            logger.info("All jobs finished.")
    
            # reset internal list for new submission round
            self.submitted_job_map = {}
            self.submitted_job_counter = 0
        else:
            logger.info("Waiting done, %d unfinished jobs in queue." % 
                        self.get_num_unfinished_jobs())

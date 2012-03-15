from util import util


class Job(object):
    """
    A job
    """

    JobStatus = util.enum('FAILED',
                          'COMPLETED',
                          'INPROGRESS',
                          'CREATED',
                          'UNKNOWN')
    """
    Job statuses:
    FAILED: job was executed and failed to complete successfully
    COMPLETED: job was executed and completed successfully
    INPROGRESS: job was created and is executing but not yet finished
    CREATED: job was created and not yet executed
    UNKNOW: job's state is unknown
    """

    def __init__(self, jobExecutionStrategy=None):
        """
        Constructor
        Job created with status JobStatus.CREATED
        @param jobExecutionStrategy A JobExecutionStrategy instance defining
                                    how the job must be executed
        """
        if not jobExecutionStrategy:
            jobExecutionStrategy = JobExecutionStrategy()
            self._jobExecutionStrategy = jobExecutionStrategy
        else:
            self._jobExecutionStrategy = jobExecutionStrategy

        self.setStatus(Job.JobStatus.CREATED)
        self._preJobs = list()
        self._jobs = list()
        self._postJobs = list()

    def execute(self):
        """
        Executes this job with the job strategy passed in constructor
        """
        self._jobExecutionStrategy.execute(job=self)

    def willExecute(self):
        """
        Indicates that execute(...) will be executed
        """
        pass

    def didExecute(self):
        """
        Indicates that execute(...) was executed
        """
        pass

    def willExecutePreJobs(self):
        """
        Indicates that executePreJobs(...) will be executed.
        """
        pass

    def didExecutePreJobs(self):
        """
        Indicates that executePreJobs(...) did execute.
        """
        pass

    def willExecutePostJobs(self):
        """
        Indicates that executePostJobs(...) will be executed.
        """
        pass

    def didExecutePostJobs(self):
        """
        Indicates that executePostJobs(...) did execute.
        """
        pass

    def willExecuteJobs(self):
        """
        Indicates that executeJobs(...) will be executed.
        """
        pass

    def didExecuteJobs(self):
        """
        Indicates that executeJobs(...) did execute.
        """
        pass

    def getStatus(self):
        """
        Returns current job status.
        @returns Valid values defined in Job.JobStatus
        """
        return self._status

    def setStatus(self, newStatus):
        """
        Updates this job's status
        @param: newStatus The new job status.
        """
        self._status = newStatus

    def preJobsCount(self):
        """
        Counts  number of pre jobs
        @return Number of pre jobs
        """
        return len(self._preJobs)

    def jobsCount(self):
        """
        Counts  number of jobs (pre and post jobs not included)
        @return Number of jobs
        """
        return len(self._jobs)

    def postJobsCount(self):
        """
        Counts  number of post jobs
        @return Number of post jobs
        """
        return len(self._postJobs)

    def getJobs(self):
        """
        Returns the list of jobs (pre and post jobs excluded)
        @return List of jobs
        """
        return self._jobs

    def getPreJobs(self):
        """
        Returns the list of pre jobs
        @return List of pre jobs
        """
        return self._preJobs

    def getPostJobs(self):
        """
        Returns the list of post jobs
        @return List of post jobs
        """
        return self._postJobs

    def addJob(self, job=None):
        """
        Adds a job to jobs
        @param: job  A job to append to the list of job.
        """
        if job:
            self._jobs.append(job)

    def addJobs(self, jobs=None):
        """
        Appends a list of jobs (i.e list of Job instances) to
        the current job list
        @param: job  A list
        """
        if jobs:
            self._jobs.extend(jobs)

    def addPreJob(self, job=None):
        """
        Adds a job to pre jobs list
        @param: job  A job to append to the list of job.
        """
        if job:
            self._preJobs.append(job)

    def addPreJobs(self, jobs=None):
        """
        Appends a list of jobs (i.e list of Job instances) to
        the current pre Jobs list
        @param: job  A list
        """
        if jobs:
            self._preJobs.extend(jobs)

    def addPostJob(self, job=None):
        """
        Adds a job to post jobs list
        @param: job  A job to append to the list of job.
        """
        if job:
            self._postJobs.append(job)

    def addPostJobs(self, jobs=None):
        """
        Appends a list of jobs (i.e list of Job instances) to
        the current post Jobs list
        @param: job  A list
        """
        if jobs:
            self._postJobs.extend(jobs)

    def getDescription(self):
        """
        Returns this job's description
        @return Job's description
        """
        return ""

    def rollback(self):
        """
        Rollbacks this job's job. Eg: if a file was moved from location A
        to B, then file at location B must be moved back at location A
        """
        pass

    def commit(self):
        """
        Commit this job.
        This implementation is empty
        WARNING: It will not be possible to rollback the job after
        this method call.
        """
        pass

from jobexecutionstrategy.jobexecutionstrategy import JobExecutionStrategy

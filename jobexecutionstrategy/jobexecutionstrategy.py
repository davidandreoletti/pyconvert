class JobExecutionStrategy(object):
    """
        Simple job execution strategy. Every job are executed.
        """

    def __init__(self):
        """
            Constructor
            """
        pass

    def execute(self, job=None):
        """
        Executes this job strategy on the job.
        This strategy is:
            execute pre jobs first if any
            then execute jobs then execute post jobs if any
        @param: job Job execution strategy
        @return Returns the Job.JobStatus.COMPLETED if all job successfully
                completed. Otherwise Job.JobStatus.FAILED
        """
        job.willExecute()
        currentJobStatus = Job.JobStatus.COMPLETED
        if job:
            if (job.preJobsCount() > 0):
                job.willExecutePreJobs()
                currentJobStatus = self.executeList(jobs=job.getPreJobs())
                job.didExecutePreJobs()

            job.willExecuteJobs()
            currentJobStatus = self.executeList(jobs=job.getJobs())
            job.didExecuteJobs()

            if (job.postJobsCount() > 0):
                job.willExecutePostJobs()
                currentJobStatus = self.executeList(jobs=job.getPostJobs())
                job.didExecutePostJobs()

            job.setStatus(newStatus=currentJobStatus)
        job.didExecute()

    def executeList(self, jobs=None):
        """
        Executes this job list
        @param: jobs A list of jobs
        @return Returns the Job.JobStatus.COMPLETED if all job
                successfully completed. Otherwise Job.JobStatus.FAILED
            """
        hasCurrentJobExecutedSuccessfully = True
        if jobs:
            for job in jobs:
                job.execute()
                if job.getStatus() != Job.JobStatus.COMPLETED:
                    hasCurrentJobExecutedSuccessfully = False

        if hasCurrentJobExecutedSuccessfully:
            return Job.JobStatus.COMPLETED
        else:
            return Job.JobStatus.FAILED

from job.job import Job

from job.job import Job
from jobexecutionstrategy import JobExecutionStrategy

class JobExecutionStrategyOnSuccessOnly(JobExecutionStrategy.JobExecutionStrategy):
    """
    A job execution strategy where the next job is executed only if the previous one executed sucessfully.
    """
    def __init__(self):
        """
            Constructor
            """
        super(JobExecutionStrategyOnSuccessOnly,self).__init__()

    def execute(self, job=None):
        """
        Executes this job strategy on the job.
        This strategy is:
        execute pre jobs first if any. If all of pre jobs executed sucessfully
        then execute jobs. If all jobs executed successfully then execute post jobs if any.
        @param: job Job execution strategy
        @return Returns the Job.JobStatus.COMPLETED if all pre post, jobs, post jobs successfully completed. Otherwise Job.JobStatus.FAILED
        """
        job.willExecute()
        currentJobStatus = Job.JobStatus.COMPLETED
        if (job.preJobsCount() > 0):
            job.willExecutePreJobs()
            currentJobStatus = self.executeList(jobs=job.getPreJobs())
            job.didExecutePreJobs()
        
        if currentJobStatus == Job.JobStatus.COMPLETED:
            job.willExecuteJobs()
            currentJobStatus = self.executeList(jobs=job.getJobs())
            job.didExecuteJobs()
            
            if currentJobStatus == Job.JobStatus.COMPLETED:
                if (job.postJobsCount() > 0):
                    job.willExecutePostJobs()
                    currentJobStatus = self.executeList(jobs=job.getPostJobs())
                    job.didExecutePostJobs()
        
        job.setStatus(newStatus=currentJobStatus)
        job.didExecute()

    def executeList(self, jobs=None):
        """
        Executes the job list.
        @param: jobs List of jobs
        @return Returns the Job.JobStatus.COMPLETED if all job successfully completed. Otherwise Job.JobStatus.FAILED AND the last job executed is the failed one. Remaining ones have not been executed
        """
        if jobs:
            hasCurrentJobExecutedSuccessfully = True
            it = iter(jobs)
            try:
                job = it.next()
                while hasCurrentJobExecutedSuccessfully and job:
                    hasCurrentJobExecutedSuccessfully = False
                    job.execute()
                    if job.getStatus() == Job.JobStatus.COMPLETED:
                        hasCurrentJobExecutedSuccessfully = True
                    job = it.next()
            except StopIteration:
                if hasCurrentJobExecutedSuccessfully:
                    return Job.JobStatus.COMPLETED
                else:
                    return Job.JobStatus.FAILED


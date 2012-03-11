class JobExecutor:
    """
    Executes jobs
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def addJobMonitor(self, jobMonitor):
        """
        Adds a JobMonitor
        @param: JobMonitor A JobMonitor instance
        """
        self._jobMonitor = jobMonitor
        return self

    def execute(self, job):
        """
        Executes a job
        @param: job Job instance
        """
        job.execute()

import os

from job import Job
from constant.constant import Constant

loggerCLRunnerRuntime = Constant.getRuntimeLogger()


class DeleteFileJob(Job):
    """
    A job to transcode/convert a media file into another media file
    """

    def __init__(self, filename=None):
        """
        Constructor
        @param: filename File to delete
        """
        super(DeleteFileJob, self).__init__()
        self._filename = filename

    def execute(self):
        self.willExecute()
        # Run command line
        os.remove(self._filename)
        self._status = Job.JobStatus.COMPLETED
        self.didExecute()

    def willExecute(self):
        """
        Indicates that execute(...) will be executed
        """
        loggerCLRunnerRuntime.info("Deleting: " + str(self._filename))

    def didExecute(self):
        """
        Indicates that execute(...) was executed
        """
        loggerCLRunnerRuntime.info("Finished: Status " + ("COMPLETED"
        if (self._status == Job.JobStatus.COMPLETED) else "FAILED"))

import os
import shutil

from job import Job
from constant.constant import Constant

loggerCLRunnerRuntime = Constant.getRuntimeLogger()

class CopyFileJob(Job):
    """
        A job to copy a file
        """

    def __init__(self,sourceFileName=None,destinationFileName=None):
        """
            Constructor
            @param: filename File to delete
            """
        super(CopyFileJob, self).__init__()
        self._sourceFileName = sourceFileName
        self._destinationFileName = destinationFileName

    def execute(self):
        self.willExecute()
        # Copy file
        shutil.copy(self._sourceFileName, self._destinationFileName)
        self._status = Job.JobStatus.COMPLETED
        self.didExecute()

    def willExecute(self):
        """
        Indicates that execute(...) will be executed
        """
        loggerCLRunnerRuntime.info("Backing up: "+str(self._sourceFileName) + " to "+str(self._destinationFileName))

    def didExecute(self):
        """
        Indicates that execute(...) was executed
        """
        loggerCLRunnerRuntime.info("Finished: Status "+( "COMPLETED" if (self._status == Job.JobStatus.COMPLETED) else "FAILED"))


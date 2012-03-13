import os
import shutil

from job import Job
from constant.constant import Constant

loggerCLRunnerRuntime = Constant.getRuntimeLogger()


class CopyFileJob(Job):
    """
    A job to copy a file
    """

    def __init__(self, sourceFileName=None, destinationFileName=None):
        """
        Constructor
        @param: sourceFilename Source file to copy
        @param: destinationFilename Destination file to copy to
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
        loggerCLRunnerRuntime.info("Backing up: " + str(self._sourceFileName) +
                                   " to " + str(self._destinationFileName))

    def didExecute(self):
        loggerCLRunnerRuntime.info("Finished: Status " + ("COMPLETED" if
        (self._status == Job.JobStatus.COMPLETED) else "FAILED"))

import os
import shutil

from job import Job
from constant.constant import Constant
from util import util

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
        # Filename with spaces on Unix
        sourceFileName = util.escapePathForOSIndependentShell(sourceFileName)
        self._sourceFileName = sourceFileName
        # Filename with spaces on Unix
        destinationFileName = util.escapePathForOSIndependentShell(destinationFileName)
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

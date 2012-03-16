from job import Job
from constant.constant import Constant

loggerCLRunnerRuntime = Constant.getRuntimeLogger()


class ConverterJob(Job):
    """
    A job to transcode/convert a media file into another media file
    """

    def __init__(self, clibuilder=None, clirunner=None):
        """
        Constructor
        @param: clibuilder CLGenerator instance generating the command line
        @param: clirunner CLRunner instance to run the command line
                          built with CLGenerator
        """
        super(ConverterJob, self).__init__()
        self._clibuilder = clibuilder
        self._clirunner = clirunner

    def execute(self):
        self.willExecute()
        # Run command line
        cli = self._clibuilder.tocl()
        self._clirunner.run(cli)
        cliRunnerReturnCode = self._clirunner.returnCode()
        cliBuilderReturnCode = self._clibuilder.getCompletedReturnCode()
        if cliRunnerReturnCode == cliBuilderReturnCode:
            self._status = Job.JobStatus.COMPLETED
        else:
            self._status = Job.JobStatus.FAILED
        self.didExecute()

    def willExecute(self):
        loggerCLRunnerRuntime.info("Executing:" + str(self._clibuilder.tocl()))

    def didExecute(self):
        loggerCLRunnerRuntime.info("Finished: Status " + ("COMPLETED" if
        (self._status == Job.JobStatus.COMPLETED) else "FAILED"))

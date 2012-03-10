from job import Job
from constant.constant import Constant

loggerCLRunnerRuntime = Constant.getRuntimeLogger()

class ConverterJob(Job):
    """
        A job to transcode/convert a media file into another media file
        """

    def __init__(self,clibuilder=None,clirunner=None):
        """
            Constructor
            @param: clibuilder CLGenerator instance
            @param: clirunner CLRunner instance to run cli built with CLGenerator
            """
        super(ConverterJob, self).__init__()
        self._clibuilder = clibuilder
        self._clirunner = clirunner

    def execute(self):
        self.willExecute()
        # Run command line
        cli=self._clibuilder.tocl()
        self._clirunner.run(cli)
	if self._clirunner.returnCode() == self._clibuilder.getCompletedReturnCode():
		self._status = Job.JobStatus.COMPLETED
	else:
		self._status = Job.JobStatus.FAILED
        self.didExecute()

    def willExecute(self):
        """
        Indicates that execute(...) will be executed
        """
        loggerCLRunnerRuntime.info("Executing:"+str(self._clibuilder.tocl()))

    def didExecute(self):
        """
        Indicates that execute(...) was executed
        """
        loggerCLRunnerRuntime.info("Finished: Status "+( "COMPLETED" if (self._status == Job.JobStatus.COMPLETED) else "FAILED"))

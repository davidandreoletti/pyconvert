from job import Job
from jobexecutionstrategy.jobexecutionstrategyonsuccessonly import JobExecutionStrategyOnSuccessOnly


class OnSuccessOnlyConverterJob(Job):
    """
    Execute this job with JobExecutionStrategyOnSuccessOnly execution strategy
    """

    def __init__(self):
        """
        Constructor
        Job created with JobExecutionStrategyOnSuccessOnly execution strategy
        """
        super(OnSuccessOnlyConverterJob, self).__init__(
        jobExecutionStrategy=JobExecutionStrategyOnSuccessOnly())

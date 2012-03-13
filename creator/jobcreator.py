# basename >= 0.0
from os.path import basename


class JobCreator:
    """
    Generic instance to create jobs.
    Specific job creators must inherit from this class
    """

    def __init__(self):
        """
        Constructor
        """
        pass

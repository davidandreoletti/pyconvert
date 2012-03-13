import logging
import time


class Constant(object):
    """
    Application constants
    """

    LOGGER_RUNTIME = None
    """
    Runtime Logger instance
    """

    LOGGER_RUNTIME_FILEHANDLER = None
    """
    Runtime Logger's file handler instance
    """

    LOGGER_TIME = None
    """
    Timer associated to any logger
    """

    @staticmethod
    def getRuntimeLogger():
        """
        @return Runtimer logger instance
        """
        if not Constant.LOGGER_RUNTIME:
            Constant.LOGGER_RUNTIME = logging.getLogger("runtime")
            Constant.LOGGER_RUNTIME.setLevel(logging.DEBUG)
            rfh = Constant.getRuntimeFileHandler()
            Constant.LOGGER_RUNTIME.addHandler(rfh)
            Constant.LOGGER_RUNTIME.addHandler(logging.StreamHandler())
        return Constant.LOGGER_RUNTIME

    @staticmethod
    def getRuntimeFileHandler():
        """
        @return Runtime's file handler
        """
        if not Constant.LOGGER_RUNTIME_FILEHANDLER:
            lrf = logging.Formatter('%(message)s')
            fileName = "runtime-" + str(Constant.getLoggerTime()) + ".log"
            lrfh = logging.FileHandler(fileName,
                                        mode='w',
                                        encoding="UTF-8")
            Constant.LOGGER_RUNTIME_FILEHANDLER = lrfh
            Constant.LOGGER_RUNTIME_FILEHANDLER.setFormatter(lrf)
        return Constant.LOGGER_RUNTIME_FILEHANDLER

    @staticmethod
    def getLoggerTime():
        """
        @return Logger's time
        """
        if not Constant.LOGGER_TIME:
            Constant.LOGGER_TIME = time.time()
        return Constant.LOGGER_TIME

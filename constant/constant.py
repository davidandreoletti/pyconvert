import logging
import time


class Constant(object):
    """
    Create jobs
    """
    LOGGER_RUNTIME = None
    LOGGER_RUNTIME_FILEHANDLER = None
    LOGGER_TIME = None

    @staticmethod
    def getRuntimeLogger():
        if not Constant.LOGGER_RUNTIME:
            Constant.LOGGER_RUNTIME = logging.getLogger("runtime")
            Constant.LOGGER_RUNTIME.setLevel(logging.DEBUG)
            rfh = Constant.getRuntimeFileHandler()
            Constant.LOGGER_RUNTIME.addHandler(rfh)
            Constant.LOGGER_RUNTIME.addHandler(logging.StreamHandler())
        return Constant.LOGGER_RUNTIME

    @staticmethod
    def getRuntimeFileHandler():
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
        if not Constant.LOGGER_TIME:
            Constant.LOGGER_TIME = time.time()
        return Constant.LOGGER_TIME

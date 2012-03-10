import logging
import time

class Constant(object):
    """
    Create jobs
    """
    LOGGER_RUNTIME=None
    LOGGER_RUNTIME_FILEHANDLER=None
    LOGGER_TIME=None

    @staticmethod
    def getRuntimeLogger():
        if not Constant.LOGGER_RUNTIME:
            Constant.LOGGER_RUNTIME = logging.getLogger("runtime")
            Constant.LOGGER_RUNTIME.setLevel(logging.DEBUG)
            Constant.LOGGER_RUNTIME.addHandler(Constant.getRuntimeFileHandler())
            Constant.LOGGER_RUNTIME.addHandler(logging.StreamHandler())
        return Constant.LOGGER_RUNTIME

    @staticmethod
    def getRuntimeFileHandler():
        if not Constant.LOGGER_RUNTIME_FILEHANDLER:
            loggerRuntimeFormatter = logging.Formatter('%(message)s')
            Constant.LOGGER_RUNTIME_FILEHANDLER = logging.FileHandler("runtime-"+str(Constant.getLoggerTime())+".log", mode='w', encoding="UTF-8")
            Constant.LOGGER_RUNTIME_FILEHANDLER.setFormatter(loggerRuntimeFormatter)
        return Constant.LOGGER_RUNTIME_FILEHANDLER



    @staticmethod
    def getLoggerTime():
        if not Constant.LOGGER_TIME:
            Constant.LOGGER_TIME = time.time()
        return Constant.LOGGER_TIME

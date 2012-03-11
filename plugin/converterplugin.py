class ConverterPlugin(object):
    def __init__(self):
        """
        Constructor
        """
        pass

    def canConvert(self, filename):
        return False

    def create(self, sourceMediaFile=None):
        pass

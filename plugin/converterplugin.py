class ConverterPlugin(object):
    """
    A converter Plugin
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    def canConvert(self, filename):
        """
        Indicates if a filename can be convert with this plugin
        @param filename Filename of file to convert
        @return True if file can be converted. False otherwise.
        """
        return False

    def create(self, sourceMediaFile=None):
        """
        Create a job to convert the source file
        @param sourceMediaFile Source MediaFile object
        @return Job to convert file or empty Job instance
        """
        pass

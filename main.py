import sys

# os >= 2.3
import os

# tempfile >=
import tempfile

# OptionParser >= 2.3
from optparse import OptionParser

import pdb
#pdb.set_trace()

from creator.convertjobcreator import ConvertJobCreator
from monitor.jobmonitor import JobMonitor
from executor.jobexecutor import JobExecutor


def main():
    """
    Application main function
    Usage: this_script.py -h
    """
    #  Parse CLI parameters
    parser = OptionParser(version="1.0")
    mdHelpMessage = ("Directory containing media files to convert."
                    + "Default value: ./")
    parser.add_option("--md",
                      "--mediaDirectory",
                      action="store",
                      type="string",
                      dest="mediaDirectoryPath",
                      default="./",
                      help=mdHelpMessage)
    parser.add_option("--mt",
                      "--mediaType",
                      action="store",
                      type="string",
                      dest="mediaType",
                      default="all",
                      help="Media type to convert. Default value: all")

    (options, args) = parser.parse_args()

    # Create jobs
    convertJobCreator = ConvertJobCreator()
    videoFileExtensions = ["avi", "mov"]
    imageFileExtensions = ["jpg", "png"]
    masterJob = convertJobCreator.createJobFromMediaDirectory(options.mediaDirectoryPath,
                                                              videoFileExtensions,
                                                              imageFileExtensions)

    # Monitore jobs
    jobMonitor = JobMonitor()

    # Executes jobs
    jobExecutor = JobExecutor()
    jobExecutor.addJobMonitor(jobMonitor)
    jobExecutor.execute(masterJob)

#Done

if __name__ == '__main__':
    main()

import os
from os.path import basename
import subprocess
import inspect
import string

from job.job import Job
from mediafile.mediafile import MediaFile
from plugin.apertureconverterplugin import ApertureConverterPlugin

import pdb
#pdb.set_trace()


class ConvertJobCreator(object):
    """
    Convert Job Creator.
    Creates ConverterJob instances
    """

    def __init__(self):
        """
        Constructor
        """
        self._plugins = list()
        self._plugins.append(ApertureConverterPlugin())

    def createJobFromMediaDirectory(self,
                                    mediaDirectoryPath,
                                    videoFileExtensions,
                                    imageFileExtensions):
        """
        Creates a job to convert all supported media files. 
        @param: mediaDirectoryPath Path to media directory
        @param: videoFileExtensions List of video file extensions
        @param: imageFileExtensions List of audio file extensions
        @return: a Job instance containing all jobs to execute.
        """
        filenames = list()
        selectedVideoFilenames = list()
        selectedImageFilenames = list()
        # Retrieve list of all files in directory
        for root, dirs, files in os.walk(os.path.abspath(mediaDirectoryPath),
                                         topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                # Filename with spaces on Unix
                filename = string.replace(filename, " ", "\ ")  
                filenames.append(filename)

        # Filter based on several criteriae
        for filename in filenames:
            fileExtension = os.path.splitext(filename)[1][1:].strip()
            fileNameWithoutExtension = os.path.splitext(filename)[0].strip()
            fileBasenameWithoutExtension = basename(fileNameWithoutExtension)
            fileExtensionLowerCase = fileExtension.lower()
            # Accept only non hidden files with specific file extension
            if (len(fileBasenameWithoutExtension) > 0 and
                    len(fileExtensionLowerCase) > 0):
                if fileExtensionLowerCase in videoFileExtensions:
                    selectedVideoFilenames.append(filename)
                elif fileExtensionLowerCase in imageFileExtensions:
                    selectedImageFilenames.append(filename)

        masterJob = Job()
        videoJob = self.createJobFromVideoFiles(selectedVideoFilenames)
        masterJob.addJob(videoJob)
        imageJob = self.createJobFromImageFiles(selectedImageFilenames)
        masterJob.addJob(imageJob)
        return masterJob

    def createJobFromVideoFiles(self, filenames=None):
        """
        Create a job containing all videos to convert
        @param: filenames List of video files
        @return: a Job instance containing all videos to convert
        """
        masterJob = Job()
        for filename in filenames:
            job = self.createJobFromVideoFile(filename)
            masterJob.addJob(job)
        return masterJob

    def createJobFromVideoFile(self, filename=None):
        """
        Create a job for the file specified
        @param: filename A video file
        @return: a Job instance containing the video file to convert
        """
        for plugin in self._plugins:
            if plugin.canConvert(filename):
                sourceMedia = plugin.probeVideo(filename)
                mediaFile = MediaFile()
                mediaFile.setFileName(filename)
                mediaFile.setVideoStreams(sourceMedia.get("video"))
                mediaFile.setAudioStreams(sourceMedia.get("audio"))
                return plugin.createVideoJob(sourceMediaFile=mediaFile)
            else:
                return Job()

    def createJobFromImageFiles(self, filenames=None):
        """
        Create a job containing all images to convert
        @param: filenames List of images files
        @return: a Job instance containing all images to convert
        """
        masterJob = Job()
        for filename in filenames:
            job = self.createJobFromImageFile(filename)
            masterJob.addJob(job)
        return masterJob

    def createJobFromImageFile(self, filename=None):
        """
        Create a job for the file specified
        @param: filename An image file
        @return: a Job instance containing the image file to convert
        """
        for plugin in self._plugins:
            if plugin.canConvert(filename):
                sourceMedia = plugin.probeImage(filename)
                mediaFile = MediaFile()
                mediaFile.setFileName(filename)
                mediaFile.setImageStreams(sourceMedia.get("image"))
                return plugin.createImageJob(sourceMediaFile=mediaFile)
            else:
                return Job()

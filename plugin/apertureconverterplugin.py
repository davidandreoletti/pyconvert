import os
import os.path
import logging
import sys
import traceback

from constant.constant import Constant

loggerJobCreationRuntime = Constant.getRuntimeLogger()

loggerJobCreationSuccess = logging.getLogger(__name__ + "creation-success")
loggerJobCreationSuccess.setLevel(logging.DEBUG)
ljcsFormatter = logging.Formatter('%(message)s')
ljcsfh = __name__ + "-creat-success-" + str(Constant.getLoggerTime()) + ".log"
loggerJobCreationSuccessFileHandler = logging.FileHandler(ljcsfh,
                                                          mode='w',
                                                          encoding="UTF-8")
loggerJobCreationSuccessFileHandler.setFormatter(ljcsFormatter)
loggerJobCreationSuccess.addHandler(loggerJobCreationSuccessFileHandler)
loggerJobCreationSuccess.addHandler(Constant.getRuntimeFileHandler())

loggerJobCreationSkipped = logging.getLogger(__name__ + "creation-skipped")
loggerJobCreationSkipped.setLevel(logging.DEBUG)
loggerJobCreationSkippedFormatter = logging.Formatter('%(message)s')
ljcsfh = __name__ + "-creat-skipped-" + str(Constant.getLoggerTime()) + ".log"
loggerJobCreationSkippedFileHandler = logging.FileHandler(ljcsfh,
                                                          mode='w',
                                                          encoding="UTF-8")
loggerJobCreationSkippedFileHandler.setFormatter(ljcsFormatter)
loggerJobCreationSkipped.addHandler(loggerJobCreationSkippedFileHandler)
loggerJobCreationSkipped.addHandler(Constant.getRuntimeFileHandler())

loggerJobCreationFailed = logging.getLogger(__name__ + "creation-failed")
loggerJobCreationFailed.setLevel(logging.DEBUG)
loggerJobCreationFailedFormatter = logging.Formatter('%(message)s')
ljcffh = __name__ + "-creat-failed-" + str(Constant.getLoggerTime()) + ".log"
loggerJobCreationFailedFileHandler = logging.FileHandler(ljcffh,
                                                         mode='w',
                                                         encoding="UTF-8")
loggerJobCreationFailedFileHandler.setFormatter(ljcsFormatter)
loggerJobCreationFailed.addHandler(loggerJobCreationFailedFileHandler)
loggerJobCreationFailed.addHandler(Constant.getRuntimeFileHandler())

import subprocess

from mediafile.mediafile import MediaFile
from stream.videostream import VideoStream
from stream.audiostream import AudioStream
from stream.imagestream import ImageStream
from handbrake.cl.handbrakeclgenerator import HandbrakeCLGenerator
from ffmpeg.cl.ffmpegclgenerator import FFMPEGCLGenerator
from ffprobe.cl.ffprobeclgenerator import FFPROBECLGenerator
from ffprobe.parser.ffprobeparser import FFprobeParser
from identify.cl.identifyclgenerator import IdentifyCLGenerator
from convert.cl.convertclgenerator import ConvertCLGenerator
#import pdb;pdb.set_trace()
from identify.parser.identifyparser import IdentifyParser
from cl.runner.clrunner import CLRunner
from job.job import Job
from job.converterjob import ConverterJob
from job.deletefilejob import DeleteFileJob
from job.copyfilejob import CopyFileJob
from job.onsuccessonlyconverterjob import OnSuccessOnlyConverterJob
from plugin.converterplugin import ConverterPlugin


class ApertureConverterPlugin(ConverterPlugin):

    SUPPORTED_FILE_EXTENSION = ["avi", "mov", "jpeg", "jpg"]

    def __init__(self):
        super(ApertureConverterPlugin, self).__init__()
        pass

    def canConvert(self, filename):
        fileExtension = os.path.splitext(filename)[1][1:].strip()
        fileBasename = os.path.splitext(filename)[0].strip()
        fileBasenameWithoutExtension = os.path.basename(fileBasename)
        fileExtensionLowerCase = fileExtension.lower()
        fileExtensions = ApertureConverterPlugin.SUPPORTED_FILE_EXTENSION
        if fileExtensionLowerCase in fileExtensions:
            return True
        else:
            return False

    def createVideoJob(self, sourceMediaFile=None):
        sourceVideoMediaStreams = sourceMediaFile.getVideoStreams()
        sourceAudioMediaStreams = sourceMediaFile.getAudioStreams()
        masterJob = None
        hanbrakeDestinationMediaFile = MediaFile()
        ffmpegSourceMediaFile = MediaFile()
        ffmpegDestinationMediaFile = MediaFile()
        destinationHandbrakeVideoStreams = list()
        destinationHandbrakeAudioStreams = list()
        destinationHandbrakeVideoStream = None
        destinationHandbrakeAudioStream = None

        destinationFFMPEGVideoStreams = list()
        destinationFFMPEGAudioStreams = list()
        destinationFFMPEGVideoStream = None
        destinationFFMPEGAudioStream = None

        # Source video attributes
        sVWidth = None
        sVHeight = None
        sVCodecName = None
        sVCodecTag = None
        sVFramerateMin = None
        # Source audio attributes
        sACodecName = None
        sACodecTag = None
        sABitPerSample = None

        # Handbrake Destination video attributes
        dVHandbrakeCodecName = None
        dVHandbrakeStreamIndex = None
        dVHandbrakeWidth = None
        dVHandbrakeHeight = None
        dVHandbrakeQuality = None
        # Handbrake  Destination audio attributes
        dAHandbrakeStreamIndex = None
        dAHandbrakeSampleRate = None
        dAHandbrakeCodecName = None

        # FFMPEG Destination video attributes
        dVFFMPEGCodecName = None
        # FFMPEG  Destination audio attributes
        dAFFMPEGCodecName = None

        countSourceVideoStreams = len(sourceVideoMediaStreams)
        if countSourceVideoStreams == 1:
            vmsKey = sourceVideoMediaStreams.keys()[0]
            vms = sourceVideoMediaStreams[vmsKey]

            sVWidth = vms.getWidth()
            sVHeight = vms.getHeight()
            sVCodecName = vms.getCodecName()
            sVCodecTag = vms.getCodecTag()
            sVFramerateMin = vms.getFramerateMin()
            sACodecName = None
            sACodecTag = None
            sABitPerSample = None
            dVHandbrakeWidth = sVWidth
            dVHandbrakeHeight = sVHeight

            loggerCameraSourceType = "Not identified"
            skippedJobCreation = True
            skippedReason = ""

            countSourceAudioStreams = len(sourceAudioMediaStreams)
            if countSourceVideoStreams == 1:
                amsKey = sourceAudioMediaStreams.keys()[0]
                ams = sourceAudioMediaStreams[amsKey]
                sACodecName = ams.getCodecName()
                sACodecTag = ams.getCodecTag()
                sABitPerSample = ams.getBitPerSample()
                dAHandbrakeStreamIndex = "1"
                dAHandbrakeSampleRate = ams.getSampleRate()
            else:
                logger.warn("NOTE:" +
                            sourceMediaFile.getFileName() +
                            ": " +
                            str(countSourceVideoStreams) +
                            " audio stream found.")

            # Select appropriate destination media file convertion settings
            # Nikon D3100
            if(sVWidth >= 1280 and sVHeight >= 720 and
                sVCodecName == "h264" and sVCodecTag == "0x31637661" and
                sACodecName == "pcm_s16le" and sACodecTag == "0x74776f73" and
                sABitPerSample == "16"):
                evfH264 = HandbrakeCLGenerator.ENCODER_VIDEO_FORMAT_H264
                dVHandbrakeCodecName = evfH264
                dVHandbrakeStreamIndex = "0"
                dVHandbrakeQuality = "25"
                dVHandbrakeWidth = 1280
                dVHandbrakeHeight = 720
                eafFAAC = HandbrakeCLGenerator.ENCODER_AUDIO_FORMAT_FAAC
                dAHandbrakeCodecName = eafFAAC
                cfMP4 = HandbrakeCLGenerator.CONTAINER_FORMAT_MP4
                hanbrakeDestinationMediaFile.setContainerType(cfMP4)

                dVFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_VIDEO_FORMAT_COPY
                dAFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_AUDIO_FORMAT_COPY

                loggerCameraSourceType = "Nikon D3100"
                skippedJobCreation = False

            # Canon Nexus 700
            elif(sVWidth == 320 and sVHeight == 240 and
                sVCodecName == "mjpeg" and sVCodecTag == "0x47504a4d" and
                sACodecName == "pcm_u8" and sACodecTag == "0x0001" and
                sABitPerSample == "8"):
                evfH264 = HandbrakeCLGenerator.ENCODER_VIDEO_FORMAT_H264
                dVHandbrakeCodecName = evfH264
                dVHandbrakeStreamIndex = "0"
                dVHandbrakeQuality = "25"
                cfMP4 = HandbrakeCLGenerator.CONTAINER_FORMAT_MP4
                hanbrakeDestinationMediaFile.setContainerType(cfMP4)

                dVFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_VIDEO_FORMAT_COPY
                dAFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_AUDIO_FORMAT_COPY

                loggerCameraSourceType = "Canon Nexus 700"
                skippedJobCreation = False

            # iPhone 3GS (NOT MBP 2007 iSight)
            elif(sVWidth == 480 and sVHeight == 360 and
                 sVCodecName == "h264" and sVCodecTag == "0x31637661" and
                 sACodecName == "aac" and sACodecTag == "0x6134706d" and
                 sABitPerSample == "0"):
                evfH264 = HandbrakeCLGenerator.ENCODER_VIDEO_FORMAT_H264
                dVHandbrakeCodecName = evfH264
                dVHandbrakeStreamIndex = "0"
                dVHandbrakeQuality = "30"
                eafFAAC = HandbrakeCLGenerator.ENCODER_AUDIO_FORMAT_FAAC
                dAHandbrakeCodecName = eafFAAC
                # quality=25 best quality=35 worst
                cfMP4 = HandbrakeCLGenerator.CONTAINER_FORMAT_MP4
                hanbrakeDestinationMediaFile.setContainerType(cfMP4)

                dVFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_VIDEO_FORMAT_COPY
                dAFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_AUDIO_FORMAT_COPY

                loggerCameraSourceType = "iPhone 3GS"
                skippedJobCreation = False

            # MBP 2010 iSight
            elif(sVWidth == 320 and sVHeight == 240 and
                 sVCodecName == "mjpeg" and sVCodecTag == "" and
                 sACodecName == "pcm_u8" and sACodecTag == "" and
                 sABitPerSample == "8"):
                evfH264 = HandbrakeCLGenerator.ENCODER_VIDEO_FORMAT_H264
                dVHandbrakeCodecName = evfH264
                dVHandbrakeStreamIndex = "0"
                dVHandbrakeQuality = "25"
                eafFAAC = HandbrakeCLGenerator.ENCODER_AUDIO_FORMAT_FAAC
                dAHandbrakeCodecName = eafFAAC
                cfMP4 = HandbrakeCLGenerator.CONTAINER_FORMAT_MP4
                hanbrakeDestinationMediaFile.setContainerType(cfMP4)

                dVFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_VIDEO_FORMAT_COPY
                dAFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_AUDIO_FORMAT_COPY

                loggerCameraSourceType = "Macbook Pro iSight 2010"
                skippedJobCreation = False

            # Unknown
            elif(sVWidth == 640 and sVHeight == 480 and
                 sVCodecName == "mjpeg" and sVCodecTag == "" and
                 sACodecName == "pcm_mulaw" and sACodecTag == "" and
                 sABitPerSample == "8"):
                evfH264 = HandbrakeCLGenerator.ENCODER_VIDEO_FORMAT_H264
                dVHandbrakeCodecName = evfH264
                dVHandbrakeStreamIndex = "0"
                dVHandbrakeQuality = "25"
                eafFAAC = HandbrakeCLGenerator.ENCODER_AUDIO_FORMAT_FAAC
                dAHandbrakeCodecName = eafFAAC
                cfMP4 = HandbrakeCLGenerator.CONTAINER_FORMAT_MP4
                hanbrakeDestinationMediaFile.setContainerType(cfMP4)

                dVFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_VIDEO_FORMAT_COPY
                dAFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_AUDIO_FORMAT_COPY

                loggerCameraSourceType = "Unknown0"
                skippedJobCreation = False

            # Panasonic DMC FX-36
            elif(sVWidth == 640 and sVHeight == 480 and
                 sVCodecName == "mjpeg" and sVCodecTag == "0x6765706a" and
                 sACodecName == "pcm_u8" and sACodecTag == "0x20776172" and
                 sABitPerSample == "8"):
                evfH264 = HandbrakeCLGenerator.ENCODER_VIDEO_FORMAT_H264
                dVHandbrakeCodecName = evfH264
                dVHandbrakeStreamIndex = "0"
                dVHandbrakeQuality = "27"
                eafFAAC = HandbrakeCLGenerator.ENCODER_AUDIO_FORMAT_FAAC
                dAHandbrakeCodecName = eafFAAC
                # quality=25 best quality=35 worst
                cfMP4 = HandbrakeCLGenerator.CONTAINER_FORMAT_MP4
                hanbrakeDestinationMediaFile.setContainerType(cfMP4)

                dVFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_VIDEO_FORMAT_COPY
                dAFFMPEGCodecName = FFMPEGCLGenerator.ENCODER_AUDIO_FORMAT_COPY

                loggerCameraSourceType = "Panasonic DMC FX-36"
                skippedJobCreation = False
            # Unknown 1
            elif(sVCodecName == None and sVCodecTag == None and
                 sACodecName == "aac" and sACodecTag == "0x6134706d" and
                 sABitPerSample == "0"):
                # No need to re-encode
                skippedJobCreation = True
                skippedReason = "No need to re-encode"
            else:
                skippedJobCreation = True
                skippedReason = ("No suitable converter configuration found. "
                                + "Missing a convertion case ? "
                                + "New video file ?" )

            if not skippedJobCreation:
                try:
                    masterJob = OnSuccessOnlyConverterJob()
                    # Convert with HandBrake as Job #1
                    destinationHandbrakeVideoStream = VideoStream(codecName=dVHandbrakeCodecName,
                                                                  streamIndex=dVHandbrakeStreamIndex,
                                                                  framerateMin=sVFramerateMin,
                                                                  width=dVHandbrakeWidth,
                                                                  height=dVHandbrakeHeight,
                                                                  quality=dVHandbrakeQuality)
                    destinationHandbrakeAudioStream = AudioStream(streamIndex=dAHandbrakeStreamIndex,
                                                                  sampleRate=dAHandbrakeSampleRate,
                                                                  codecName=dAHandbrakeCodecName)
                    destinationHandbrakeVideoStreams.append(destinationHandbrakeVideoStream)
                    destinationHandbrakeAudioStreams.append(destinationHandbrakeAudioStream)
                    hanbrakeDestinationMediaFile.setVideoStreams(destinationHandbrakeVideoStreams)
                    hanbrakeDestinationMediaFile.setAudioStreams(destinationHandbrakeAudioStreams)
                    handbrakeDestinationFileName = sourceMediaFile.getFileName() + ".tmp." + str(hanbrakeDestinationMediaFile.getContainerType())
                    hanbrakeDestinationMediaFile.setFileName(handbrakeDestinationFileName)
                    handbrakeCLIBuilder = HandbrakeCLGenerator.createFrom(sourceMediaFile=sourceMediaFile, destinationMediaFile=hanbrakeDestinationMediaFile)
                    handbrakeCLIBuilder.addLooseAnamorphic()
                    handbrakeCLIBuilder.addVerbosity()
                    handbrakeCLIRunner = CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    masterJob.addJob(ConverterJob(clibuilder=handbrakeCLIBuilder, clirunner=handbrakeCLIRunner))
                    loggerJobCreationRuntime.info("Handbrake cl:" + str(handbrakeCLIBuilder.tocl()))

                    # Convert with FFMpeg as Job #2
                    destinationFFMPEGVideoStream = VideoStream(codecName=dVFFMPEGCodecName)
                    destinationFFMPEGAudioStream = AudioStream(codecName=dAFFMPEGCodecName)

                    ffmpegSourceMediaFile.setFileName(hanbrakeDestinationMediaFile.getFileName())
                    ffmpegDestinationMediaFile.setFileName(sourceMediaFile.getFileName())
                    destinationFFMPEGVideoStreams.append(destinationFFMPEGVideoStream)
                    destinationFFMPEGAudioStreams.append(destinationFFMPEGAudioStream)
                    ffmpegDestinationMediaFile.setVideoStreams(destinationFFMPEGVideoStreams)
                    ffmpegDestinationMediaFile.setAudioStreams(destinationFFMPEGAudioStreams)
                    ffmpegCLIBuilder = FFMPEGCLGenerator.createFrom(sourceMediaFile=ffmpegSourceMediaFile, destinationMediaFile=ffmpegDestinationMediaFile)
                    ffmpegCLIBuilder.addOverwriteOutputFileWithoutAsking()
                    ffmpegCLIRunner = CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    loggerJobCreationRuntime.info("ffmpeg cl:" + str(handbrakeCLIBuilder.tocl()))

                    masterJob.addJob(ConverterJob(clibuilder=ffmpegCLIBuilder, clirunner=ffmpegCLIRunner))
                    # Delete temporary file as Job #3
                    masterJob.addJob(DeleteFileJob(filename=handbrakeDestinationFileName))
                    loggerJobCreationRuntime.info("Will delete file:" + str(handbrakeDestinationFileName))
                    loggerJobCreationSuccess.info("JOB_CREATION_SUCCESS:" + sourceMediaFile.getFileName() + ": Type:" + loggerCameraSourceType)
                except BaseException:
                    loggerJobCreationFailed.exception("JOB_CREATION_FAILED:" + sourceMediaFile.getFileName() + ": Type:" + loggerCameraSourceType + "Exception :")
            else:
                loggerJobCreationSkipped.info("JOB_CREATION_SKIPPED:" +
                                              sourceMediaFile.getFileName() +
                                              ": Type:" + loggerCameraSourceType +
                                              " Reason: " + skippedReason)
        else:
            loggerJobCreationFailed.error("JOB_CREATION_FAILED:" + sourceMediaFile.getFileName() + ": Reason: 1 video stream expected. " + str(countSourceVideoStreams) + " found.")

        if not masterJob:
            masterJob = Job()  # Created only if proper convert job not created
        return masterJob

    @staticmethod
    def createVideoStream(d=None):
        """
        Creates a VideoStream object instance from dictionary of properties taken from ffprobe -show-streams's output
        @param: d Dictionary Dictionary of properties
        @return: VideoStream instance
        """
        # Convert "avg_frame_rate" string value representation into floating value: 2000/1001 ==> 1.998002
        framerateMin = ApertureConverterPlugin.getValueOrDefault(d, "avg_frame_rate")
        framerateMinValue = framerateMin
        if type(framerateMin) is str:
            numbers = framerateMin.split('/')
            if len(numbers) == 1:
                framerateMinValue = str(eval(numbers[0]))  # FIXME: Dangerous since input is not trusted. This must be sanitized.
            if len(numbers) == 2:
                framerateMinValue = str(eval(str(float(numbers[0])) + "/" + str(float(numbers[1]))))  # FIXME: Dangerous since input is not trusted. This must be sanitized.
            else:
                loggerJobCreationRuntime.error("Cannot convert " + str(framerateMin) + " into floating value")

            # Restrict precision to 3 decimal digits maximun
            framerateIdentified = False
            frameratePotentialValues = ["29.97", "25", "24", "23.976", "15", "12", "10", "5"]
            framerateIndex = 0
            countFrameratePotentialValues = len(frameratePotentialValues)
            while not framerateIdentified and framerateIndex < countFrameratePotentialValues:
                currentFramerateValue = frameratePotentialValues[framerateIndex]
                if framerateMinValue.startswith(currentFramerateValue):
                    framerateMinValue = currentFramerateValue
                    framerateIdentified = True
                framerateIndex = framerateIndex + 1

            loggerJobCreationRuntime.info("Converted value " + str(framerateMin) + "==>" + str(framerateMinValue))
        else:
            loggerJobCreationRuntime.warning("Value from ffprobe is not in expected format:" + str(framerateMin))

        return VideoStream(codecLongName=ApertureConverterPlugin.getValueOrDefault(d, "codec_long_name"),
                           codecTag=ApertureConverterPlugin.getValueOrDefault(d, "codec_tag"),
                           streamIndex=ApertureConverterPlugin.getValueOrDefault(d, "index"),
                           codecTagString=ApertureConverterPlugin.getValueOrDefault(d, "codec_tag_string"),
                           codecName=ApertureConverterPlugin.getValueOrDefault(d, "codec_name"),
                           framerateMin=framerateMinValue,
                           width=ApertureConverterPlugin.getValueOrDefault(d, "width"),
                           height=ApertureConverterPlugin.getValueOrDefault(d, "height"),
                           quality=None)

    @staticmethod
    def createAudioStream(d=None):
        """
        Creates a AudioStream object instance from dictionary of properties taken from ffprobe -show-streams's output
        @param: d Dictionary Dictionary of properties
        @return: AudioStream instance
        """
        # Convert Hz to kHz
        sampleRate = ApertureConverterPlugin.getValueOrDefault(d, "sample_rate")
        sampleRateValue = sampleRate
        if type(sampleRate) is str:
            sampleRateValue = str(float(sampleRate) / 1000.0)
        loggerJobCreationRuntime.info("Converted value " + str(sampleRate) + "==>" + str(sampleRateValue))
        return AudioStream(codecLongName=ApertureConverterPlugin.getValueOrDefault(d, "codec_long_name"),
                           codecTag=ApertureConverterPlugin.getValueOrDefault(d, "codec_tag"),
                           codecTagString=ApertureConverterPlugin.getValueOrDefault(d, "codec_tag_string"),
                           codecName=ApertureConverterPlugin.getValueOrDefault(d, "codec_name"),
                           streamIndex=ApertureConverterPlugin.getValueOrDefault(d, "index"),
                           bitPerSample=ApertureConverterPlugin.getValueOrDefault(d, "bits_per_sample"),
                           sampleRate=sampleRateValue)

    @staticmethod
    def getValueOrDefault(d, keyname):
        """
        Retrieves value associated to property name or default value if property does not exists
        @param: d Dictionary Dictionary of properties
        @param: Property name
        @return: Property value or None
        """
        return d.get(keyname, None)

    def probeVideo(self, filename=None):
        """
        Probes a video file.
        Caveat: Supports only 1 video channel and 1 audio chanel
        @param: file Video file to probe
        @return Dictionary. Key "video" contains dictionary of VideoStream objects and key "audio" contains a dictionary of AudioStream objects
        """
        loggerJobCreationRuntime.info("================================================================================")
        loggerJobCreationRuntime.info("Processing :" + str(filename))
        # Prepare CL
        ffprobeCLBuilder = FFPROBECLGenerator()
        ffprobeCLBuilder.addInputFile(filename)
        ffprobeCLBuilder.addShowStreams()
        cl = ffprobeCLBuilder.tocl()
        loggerJobCreationRuntime.info("ffprobe cl:" + str(cl))

        # Run CL
        clRunner = CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        clRunner.run(cl, shell=False)
        ffprobeRawOutput = clRunner.stdout()
        loggerJobCreationRuntime.info("ffprobe raw output:" + str(ffprobeRawOutput))
        # Parse CL output
        ffprobeParser = FFprobeParser()
        streams = ffprobeParser.parseShowStreamsOuput(ffprobeRawOutput)

        # Second pass: Build media instances
        countStreams = len(streams)
        mediaStreams = list()
        if countStreams > 0:
            for i in range(0, countStreams, 1):
                stream = streams[i]
                mediaStream = None
                if stream["codec_type"] in "video":
                    mediaStream = ApertureConverterPlugin.createVideoStream(d=stream)
                elif stream["codec_type"] in "audio":
                    mediaStream = ApertureConverterPlugin.createAudioStream(d=stream)
                mediaStreams.append(mediaStream)

        streamsMediaObjects = dict(video=dict(), audio=dict())
        for i in range(0, len(mediaStreams)):
            mediaStream = mediaStreams[i]
            streams = None
            if mediaStream.getType() in "video":
                streams = (streamsMediaObjects["video"])
            elif mediaStream.getType() in "audio":
                streams = (streamsMediaObjects["audio"])
            streams[mediaStream.getStreamIndex()] = mediaStream
        loggerJobCreationRuntime.info("ffprobe converted output:" + str(streamsMediaObjects))
        return streamsMediaObjects

    def probeImage(self, filename=None):
            """
            Probes an image
            @param: file Image file to probe
            @return Dictionary. Key "image" contains dictionary of ImageStream objects
            """
            loggerJobCreationRuntime.info("================================================================================")
            loggerJobCreationRuntime.info("Processing :" + str(filename))

            # Get Image width
            identifyCLBuilder0 = IdentifyCLGenerator()
            identifyCLBuilder0.addInputFile(filename)
            identifyCLBuilder0.addFormatOption()
            identifyCLBuilder0.addFormatWidthOption()
            cl0 = identifyCLBuilder0.tocl()
            loggerJobCreationRuntime.info("identify cl:" + str(cl0))

            clRunner0 = CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            clRunner0.run(cl0, shell=False)
            identifyCLRawOutput0 = clRunner0.stdout()

            identifyParser0 = IdentifyParser()
            width = identifyParser0.parseFormatWidthOption(identifyCLRawOutput0)

            # Get Image height
            identifyCLBuilder1 = IdentifyCLGenerator()
            identifyCLBuilder1.addInputFile(filename)
            identifyCLBuilder1.addFormatOption()
            identifyCLBuilder1.addFormatHeightOption()
            cl1=identifyCLBuilder1.tocl()
            loggerJobCreationRuntime.info("identify cl:" + str(cl1))

            clRunner1=CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            clRunner1.run(cl1, shell=False)
            identifyCLRawOutput1=clRunner1.stdout()

            identifyParser1 = IdentifyParser()
            height = identifyParser1.parseFormatHeightOption(identifyCLRawOutput1)

            # Get Image DPI X
            identifyCLBuilder2 = IdentifyCLGenerator()
            identifyCLBuilder2.addInputFile(filename)
            identifyCLBuilder2.addFormatOption()
            identifyCLBuilder2.addFormatHorizontalDPIOption()
            cl2=identifyCLBuilder2.tocl()
            loggerJobCreationRuntime.info("identify cl:" + str(cl2))

            clRunner2=CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            clRunner2.run(cl2, shell=False)
            identifyCLRawOutput2=clRunner2.stdout()

            identifyParser2 = IdentifyParser()
            dpiX = identifyParser2.parseFormatHorizontalDPIOption(identifyCLRawOutput2)

            # Get Image DPI Y
            identifyCLBuilder3 = IdentifyCLGenerator()
            identifyCLBuilder3.addInputFile(filename)
            identifyCLBuilder3.addFormatOption()
            identifyCLBuilder3.addFormatVerticalDPIOption()
            cl3=identifyCLBuilder3.tocl()
            loggerJobCreationRuntime.info("identify cl:" + str(cl3))

            clRunner3=CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            clRunner3.run(cl3, shell=False)
            identifyCLRawOutput3=clRunner3.stdout()

            identifyParser3 = IdentifyParser()
            dpiY = identifyParser3.parseFormatVerticalDPIOption(identifyCLRawOutput3)

            # Get Image Quality
            identifyCLBuilder4 = IdentifyCLGenerator()
            identifyCLBuilder4.addInputFile(filename)
            identifyCLBuilder4.addFormatOption()
            identifyCLBuilder4.addFormatQualityOption()
            cl4=identifyCLBuilder4.tocl()
            loggerJobCreationRuntime.info("identify cl:" + str(cl4))

            clRunner4=CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            clRunner4.run(cl4, shell=False)
            identifyCLRawOutput4=clRunner4.stdout()

            identifyParser4 = IdentifyParser()
            quality = identifyParser4.parseFormatQualityOption(identifyCLRawOutput4)
            imageStream = ImageStream(filename=filename,
                                      width=width,
                                      height=height,
                                      quality=quality,
                                      densityX=dpiX,
                                      densityY=dpiY)
            imageStreams = dict()
            imageStreams["0"] = imageStream
            streamsMediaObjects = dict(image=imageStreams)
            return streamsMediaObjects

    def createImageJob(self, sourceMediaFile=None):
        sourceImageStreams = sourceMediaFile.getImageStreams()
        masterJob = None
        backupDestinationMediaFile = MediaFile()
        convertDestinationMediaFile = MediaFile()
        destinationBakupImageStreams = list()
        destinationConvertImageStreams = list()

        # Source video attributes
        sIWidth = None
        sIHeight = None
        sIDPIX = None
        sIDPIY = None
        sIQuality = None

        # Handbrake Destination video attributes
        dIWidth = None
        dIHeight = None
        dIDPIX = None
        dIDPIY = None
        dIQuality = None

        countSourceImageStreams = len(sourceImageStreams)
        if countSourceImageStreams == 1:
            imsKey = sourceImageStreams.keys()[0]
            ims = sourceImageStreams[imsKey]

            sIWidth = ims.getWidth()
            sIHeight = ims.getHeight()
            sIDPIX = ims.getDensityX()[0]
            sIDPIY = ims.getDensityY()[0]
            sIQuality = ims.getQuality()
            loggerCameraSourceType = "Not identified"
            skippedJobCreation = True
            skippedReason = ""

            sIQuotientHeightWidth = float(float(sIHeight)/float(sIWidth))

            # Select appropriate destination media file convertion settings
            # Unknown1
            if(sIDPIX == 300 and sIDPIY == 300 and
               sIWidth >= 3508 and sIHeight >= 2480):
                if sIQuotientHeightWidth >= 1.0:
                    sIHeight=3508
                else:
                    dIWidth=2480
                dIQuality=95
                loggerCameraSourceType = "Unknown1"
                skippedJobCreation = False
            # Unknown2
            elif(sIWidth <= 2480 and sIHeight <= 3508):
                # No need to re-encode
                skippedJobCreation = True
                skippedReason = "No need to re-encode"
            else:
                skippedJobCreation = True
                skippedReason = "No suitable converter configuration found. Missing a convertion case ? New image file ?"

            if not skippedJobCreation:
                try:
                    masterJob = OnSuccessOnlyConverterJob()
                    # Backup file as Job #1
                    sourceBackupFileName = sourceMediaFile.getFileName()
                    destinationBackupFileName = str(sourceBackupFileName) + ".backup"
                    destinationBackupMediaFile = MediaFile()
                    destinationBackupMediaFile.setFileName(destinationBackupFileName)
                    copyFileJob = CopyFileJob(sourceFileName=sourceMediaFile.getFileName(), destinationFileName=destinationBackupMediaFile.getFileName())
                    masterJob.addJob(copyFileJob)
                    loggerJobCreationRuntime.info("Will backup file: " + str(sourceBackupFileName) + " to " + str(destinationBackupFileName))

                    # Convert with ImageMagick's mogrity tool as Job #2
                    convertSourceMediaFile = MediaFile()
                    convertSourceMediaFile.setFileName(destinationBackupFileName)
                    convertDestinationFileName = sourceMediaFile.getFileName()
                    convertDestinationMediaFile.setFileName(convertDestinationFileName)
                    destinationConvertImageStream = ImageStream(filename=convertDestinationFileName, width=dIWidth, height=sIHeight, quality=dIQuality, densityX=dIDPIX, densityY=dIDPIY)
                    destinationConvertImageStreams.append(destinationConvertImageStream)
                    convertDestinationMediaFile.setImageStreams(destinationConvertImageStreams)
                    convertCLIBuilder = ConvertCLGenerator.createResizeJobFrom(sourceMediaFile=convertSourceMediaFile, destinationMediaFile=convertDestinationMediaFile)
                    convertCLIRunner = CLRunner(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    masterJob.addJob(ConverterJob(clibuilder=convertCLIBuilder, clirunner=convertCLIRunner))
                    loggerJobCreationRuntime.info("convert cl:" + str(convertCLIBuilder.tocl()))

                    # Delete backup file as Job #3
                    masterJob.addJob(DeleteFileJob(filename=destinationBackupMediaFile.getFileName()))
                    loggerJobCreationRuntime.info("Will delete file:" + str(destinationBackupMediaFile.getFileName()))
                    loggerJobCreationSuccess.info("JOB_CREATION_SUCCESS:" + sourceMediaFile.getFileName() + ": Type:" + loggerCameraSourceType)
                except BaseException:
                    loggerJobCreationFailed.exception("JOB_CREATION_FAILED:" + sourceMediaFile.getFileName() + ": Type:" + loggerCameraSourceType + "Exception :")
            else:
                loggerJobCreationSkipped.info("JOB_CREATION_SKIPPED:" +
                                              sourceMediaFile.getFileName() +
                                              ": Type:" + loggerCameraSourceType
                                              + " Reason: " +skippedReason)			
        else:
            loggerJobCreationFailed.error("JOB_CREATION_FAILED:" + sourceMediaFile.getFileName() + ": Reason: 1 video stream expected. " + str(countSourceVideoStreams) + " found.")

        if not masterJob:
            masterJob = Job()  # Created only if proper convert job not created 
        return masterJob

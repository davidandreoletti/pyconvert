import logging

# Create loggers

runtimeLogger = logging.getLogger('runtime')
runtimeLogger.setLevel(logging.DEBUG)

jobCreationSuccessLogger = logging.getLogger('job-creation-success')
jobCreationSuccessLogger.setLevel(logging.DEBUG)

jobCreationFailureLogger = logging.getLogger('runtime')
jobCreationFailureLogger.setLevel(logging.DEBUG)

# Create formatters
runtimeFormatterStr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
runtimeFormatter = logging.Formatter(runtimeFormatterStr)
jobCreationSuccessFormatterStr = 'JOB CREATION SUCCESS:%(message)s'
jobCreationSuccessFormatter = logging.Formatter(jobCreationSuccessFormatterStr)
jobCreationFailureFormatterStr = 'JOB CREATION FAILURE:%(message)s'
jobCreationFailureFormatter = logging.Formatter(jobCreationFailureFormatterStr)

# Create handlers
runtimeFileHandler = logging.FileHandler()
runtimeConsoleHandler = logging.StreamHandler()
jobCreationSuccessHandler = logging.FileHandler()
jobCreationFailureHandler = logging.FileHandler()

# Add formatter to handler
runtimeFileHandler.setFormatter(runtimeFormatter)
runtimeConsoleHandler.setFormatter(runtimeFormatter)
jobCreationSuccessHandler.setFormatter(jobCreationSuccessHandler)
jobCreationFailureHandler.setFormatter(jobCreationFailureHandler)

# Add handler to logger
runtimeLogger
jobCreationSuccessLogger
jobCreationFailureLogger

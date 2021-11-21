import logging


class Logger:

    def __init__(self, nm):
        """
        Create Logging object
        :return:
        """
        self.logger = logging.getLogger(nm)
        # reading contents from properties file
        f = open("properties.txt", 'r')
        if f.mode == "r":
            log_level = f.read()
        if log_level == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        # Creating Formatters
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        # Creating Handlers
        file_handler = logging.FileHandler('LoggerFile.log')
        # Adding Formatters to Handlers
        file_handler.setFormatter(formatter)
        # Adding Handlers to logger
        self.logger.addHandler(file_handler)

    def add_debug_log(self, msg):
        self.logger.debug(msg)

    def add_info_log(self, msg):
        self.logger.info(msg)

    def add_warning_log(self, msg):
        self.logger.warning(msg)

    def add_exception_log(self, msg):
        self.logger.exception(msg)

    def add_error_log(self, msg):
        self.logger.error(msg)

    def add_critical_log(self, msg):
        self.logger.critical(msg)

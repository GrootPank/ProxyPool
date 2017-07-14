import logging
import os
from logging.handlers import TimedRotatingFileHandler

PWD = os.path.split(os.path.realpath(__file__))[0]
LOG_PATH = os.path.join(os.path.split(PWD)[0],"Log")


class LogHandler(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        self.name = name
        self.level = level
        super().__init__(name,level=level)
        self.__setFileHandler__()
        self.__setStreamHandler__()

    def __setFileHandler__(self):
        fileName = os.path.join(LOG_PATH,"{name}.log".format(name=self.name))
        logHandler = TimedRotatingFileHandler(fileName, when='d', interval=1, backupCount=15)
        logHandler.suffix = "%y%m%d.log"
        logHandler.setLevel(self.level)
        formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        logHandler.setFormatter(formatter)
        self.addHandler(logHandler)

    def __setStreamHandler__(self):
        logHandler = logging.StreamHandler()
        logHandler.setLevel(self.level)
        formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        logHandler.setFormatter(formatter)
        self.addHandler(logHandler)

if __name__ == '__main__':
    logger = LogHandler('test')
    logger.debug("This is debug info")
    logger.info("This is info")
    logger.error("This is error info")
    logger.critical("This is critical info")
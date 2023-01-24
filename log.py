import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import date

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s — %(funcName)s:%(lineno)d - %(message)s")
LOG_FILE = os.getcwd() + os.sep + "logs" + os.sep + "pdflogger-{0}.log".format(date.today())

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    #set level to debug
    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
    #create new handlers if they do not exist already
    if(len(logger.handlers) == 0):
        logger.addHandler(get_console_handler())
        logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

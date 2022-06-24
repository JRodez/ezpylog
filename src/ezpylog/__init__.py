# Copyright 2022, JRodez <jeremierodez@outlook.com>

import inspect
import sys
import enum
from datetime import datetime
from abc import ABC
import logging


class colors:
    NEUTRAL = "\033[97m"
    DEBUG = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[1m\033[91m'
    CRITICALMSG = '\033[4m\033[91m'
    CONTEXT = '\033[96m'
    ENDC = '\033[0m'


SUPPORTED_TYPES = [str, dict]


def dict_to_str(collection: dict, indent=0):
    return_string = ['{\n']
    if isinstance(collection, dict):
        for key, value in collection.items():
            if isinstance(value, dict) or isinstance(value, list):
                value = dict_to_str(value, indent + 1)
            else:
                value = repr(value)

            return_string.append('%s%r: %s,\n' % ('  ' * indent, key, value))
        return_string.append('%s}' % ('  ' * indent))
        return ''.join(return_string)

    elif isinstance(collection, list):
        for value in collection:
            if isinstance(value, dict) or isinstance(value, list):
                value = dict_to_str(value, indent + 1)
            else:
                value = repr(value)
            return_string.append('%s%s,\n' % ('  ' * indent, value))
        return_string.append('%s]' % ('  ' * indent))
        return ''.join(return_string)


class EzpylogFormatter(logging.Formatter):
    """A class for formatting colored logs."""

    LOG_LEVEL_COLOR = {
        "DEBUG": {'lvlprefix': colors.DEBUG, 'lvlsuffix': colors.ENDC, 'msgprefix': "", 'msgsuffix':  colors.ENDC},
        "INFO": {'lvlprefix': colors.INFO, 'lvlsuffix': colors.ENDC, 'msgprefix': "", 'msgsuffix':  colors.ENDC},
        "WARNING": {'lvlprefix': colors.WARNING, 'lvlsuffix': colors.ENDC, 'msgprefix': "", 'msgsuffix':  colors.ENDC},
        "ERROR": {'lvlprefix': colors.ERROR, 'lvlsuffix': colors.ENDC, 'msgprefix': colors.ERROR, 'msgsuffix':  colors.ENDC},
        "CRITICAL": {'lvlprefix': colors.CRITICAL, 'lvlsuffix': colors.ENDC, 'msgprefix': colors.CRITICALMSG, 'msgsuffix':  colors.ENDC},
    }

    # FORMAT = f"%(asctime)s | %(lvlprefix)s[%(levelname)s]%(lvlsuffix)s {bcolors.CONTEXT}[%(module)s.%(funcName)s]{bcolors.ENDC} %(msgprefix)s%(message)s%(msgsuffix)s"
    FORMAT = f"%(asctime)s %(lvlprefix)s[%(levelname)s]%(lvlsuffix)s {colors.CONTEXT}[%(module)s.%(funcName)s]{colors.ENDC} %(msgprefix)s%(message)s%(msgsuffix)s"

    def format(self, record):
        """Format log records with a default lvlprefix and lvlsuffix to terminal color codes that corresponds to the log level name."""
        if not hasattr(record, 'lvlprefix'):
            record.lvlprefix = self.LOG_LEVEL_COLOR.get(
                record.levelname.upper()).get('lvlprefix')

        if not hasattr(record, 'lvlsuffix'):
            record.lvlsuffix = self.LOG_LEVEL_COLOR.get(
                record.levelname.upper()).get('lvlsuffix')
        if not hasattr(record, 'msgprefix'):
            record.msgprefix = self.LOG_LEVEL_COLOR.get(
                record.levelname.upper()).get('msgprefix')

        if not hasattr(record, 'msgsuffix'):
            record.msgsuffix = self.LOG_LEVEL_COLOR.get(
                record.levelname.upper()).get('msgsuffix')
        formatter = logging.Formatter(self.FORMAT, "%d-%m-%y %H:%M:%S")
        return formatter.format(record)


class Logger(object):
    def __init__(self, name=None,  min_level: int = logging.WARNING, logfile: str = None):
        """ Initialize the logger.
        :param `min_level`: The minimum level of log to be displayed.
        :param `logfile`: The file to log to.
        """

        if not isinstance(min_level, int):
            raise ValueError('min_level must be a int')
        self._logger: logging.Logger = logging.getLogger(
        ) if name is None else logging.getLogger(name)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(EzpylogFormatter())
        self._logger.addHandler(self.stream_handler)

        if logfile is not None:
            self._logger.addHandler(logging.FileHandler(logfile))

        self._logger.setLevel(min_level)

    def log(self, msg, level: int = logging.INFO):
        """ Log a message. 
        :param `msg`: The message to be logged.
        :param `level`: The level of the message.
        :param `context`: The context of the message.
        """

        if type(msg) not in SUPPORTED_TYPES:
            try:
                text = str(msg)
            except:
                raise ValueError(
                    f"msg must be {SUPPORTED_TYPES.join(', ')} or convertable to a string")
        elif type(msg) is dict:
            text = dict_to_str(msg)
        else:
            text = msg
        splitted = text.split("\n")
        for line in splitted:
            space = '> ' if len(splitted) > 1 else ''
            self._logger.log(level, f"{space}{line}", stacklevel=2)

    def getLogger(self):
        return self._logger

    def debug(self, msg=""):
        self.log(msg, logging.DEBUG)

    def info(self, msg=""):
        self.log(msg, logging.INFO)

    def warning(self, msg=""):
        self.log(msg, logging.WARNING)

    def error(self, msg=""):
        self.log(msg, logging.ERROR)

    def critical(self, msg=""):
        self.log(msg, logging.CRITICAL)

    def close(self):
        for handler in self._logger.handlers:
            handler.close()
            self._logger.removeHandler(handler)

    def __del__(self):
        self.close()


def loggerdemo():
    print()

    a = 1234567

    logger = Logger("TestLogger", min_level=logging.DEBUG)
    logger.log("Debug message\non\nmultiple\nline", logging.DEBUG)
    logger.log("Info message")
    logger.log("Warning message", logging.WARNING)
    logger.log(f"Error message {a}", logging.ERROR)
    logger.log("Critical message", logging.CRITICAL)

    print()

    logger2 = Logger(__name__, logging.WARNING,)
    logger2.log("Debug message", logging.DEBUG)
    logger2.log("Info message", logging.INFO)
    logger2.log("Warning message", logging.WARNING)
    logger2.log(f"Error message {a}", logging.ERROR)
    logger2.log("Critical message", logging.CRITICAL)
    logger.debug({})
    print()


if __name__ == "__main__":
    loggerdemo()

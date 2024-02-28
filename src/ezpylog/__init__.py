# Copyright 2022, JRodez <jeremierodez@outlook.com>
import json
import os
from platform import python_version
import inspect
import sys
import enum
from datetime import datetime
from abc import ABC
import logging

OLD_PYTHON = True if int(python_version().split(".")[1]) < 8 else False
# OLD_PYTHON = True


ONE_LINE_CHAR    = " "
MULTI_LINE_CHAR  = "| "

if hasattr(sys, "_getframe"):

    def currentframe():
        return sys._getframe(3)


_srcfile = os.path.normcase(currentframe.__code__.co_filename)


def get_caller_name():
    stack = inspect.stack()
    fn = stack[1].filename
    fn = fn.split("/")
    if len(fn) <= 1:
        fn = fn[-1].split("\\")
    fn = fn[-1]
    return fn


def findCallerPatch(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = currentframe()
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)", None
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name, None)
        break
    return rv


class LogLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class colors:
    NEUTRAL = "\033[97m"
    DEBUG = "\033[94m"
    INFO = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    CRITICAL = "\033[1m\033[91m"
    CRITICALMSG = "\033[7m\033[91m"
    CONTEXT = "\033[96m"
    CHARACTER = "\033[2m"

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"

    ENDC = "\033[0m"


SUPPORTED_TYPES = (str, dict)


def dict_to_str(collection: dict, indent=0):
    return_string = ["{\n"]
    if isinstance(collection, dict):
        for key, value in collection.items():
            if isinstance(value, dict) or isinstance(value, list):
                value = dict_to_str(value, indent + 1)
            else:
                value = repr(value)

            return_string.append("%s%r: %s,\n" % ("  " * indent, key, value))
        return_string.append("%s}" % ("  " * indent))
        return "".join(return_string)

    elif isinstance(collection, list):
        for value in collection:
            if isinstance(value, dict) or isinstance(value, list):
                value = dict_to_str(value, indent + 1)
            else:
                value = repr(value)
            return_string.append("%s%s,\n" % ("  " * indent, value))
        return_string.append("%s]" % ("  " * indent))
        return "".join(return_string)


class EzpylogColoredFormatter(logging.Formatter):
    """A class for formatting colored logs."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.LOG_LEVEL_COLOR = {
            "DEBUG": {
                "lvlprefix": colors.DEBUG,
                "lvlsuffix": colors.ENDC,
                "msgprefix": "",
                "msgsuffix": colors.ENDC,
                "label": "DEBUG",
            },
            "INFO": {
                "lvlprefix": colors.INFO,
                "lvlsuffix": colors.ENDC,
                "msgprefix": "",
                "msgsuffix": colors.ENDC,
                "label": "INFO",
            },
            "WARNING": {
                "lvlprefix": colors.WARNING,
                "lvlsuffix": colors.ENDC,
                "msgprefix": colors.WARNING,
                "msgsuffix": colors.ENDC,
                "label": "WARNING",
            },
            "ERROR": {
                "lvlprefix": colors.ERROR,
                "lvlsuffix": colors.ENDC,
                "msgprefix": colors.ERROR,
                "msgsuffix": colors.ENDC,
                "label": "ERROR",
            },
            "CRITICAL": {
                "lvlprefix": colors.CRITICAL,
                "lvlsuffix": colors.ENDC,
                "msgprefix": colors.CRITICALMSG,
                "msgsuffix": colors.ENDC,
                "label": "CRITICAL",
            },
        }

        if "compact" in kwargs and kwargs['compact']:
            self.FORMAT = f"%(lvlprefix)s[%(levelname)5s]%(lvlsuffix)s {colors.CONTEXT}[%(funcName)-12s]{colors.ENDC} %(msgprefix)s%(message)s%(msgsuffix)s"
            self.LOG_LEVEL_COLOR["WARNING"]["label"] = "WARN"
            self.LOG_LEVEL_COLOR["CRITICAL"]["label"] = "FATAL"
        else:
            self.FORMAT = f"%(asctime)s | %(lvlprefix)s[%(levelname)8s]%(lvlsuffix)s {colors.CONTEXT}[%(module)12s.%(funcName)-16s]{colors.ENDC} %(msgprefix)s%(message)s%(msgsuffix)s"

    # FORMAT = f"%(asctime)s | %(lvlprefix)s[%(levelname)s]%(lvlsuffix)s {bcolors.CONTEXT}[%(module)s.%(funcName)s]{bcolors.ENDC} %(msgprefix)s%(message)s%(msgsuffix)s"

    def format(self, record):
        """Format log records with a default lvlprefix and lvlsuffix to terminal color codes that corresponds to the log level name."""

        if not hasattr(record, "lvlprefix"):
            record.lvlprefix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
                "lvlprefix"
            )

        if not hasattr(record, "lvlsuffix"):
            record.lvlsuffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
                "lvlsuffix"
            )
        if not hasattr(record, "msgprefix"):
            record.msgprefix = ""
            if record.msg.startswith("Traceback"):
                record.msgprefix = colors.ERROR
            elif record.msg.startswith(ONE_LINE_CHAR):
                record.msgprefix = f"{colors.CHARACTER}{ONE_LINE_CHAR}{colors.ENDC}"
                record.msg = record.msg[len(ONE_LINE_CHAR) :]
                if record.msg.startswith(MULTI_LINE_CHAR):
                    record.msgprefix += f"{colors.CHARACTER}{MULTI_LINE_CHAR}{colors.ENDC}"
                    record.msg = record.msg[len(MULTI_LINE_CHAR) :]
            record.msgprefix += self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
                "msgprefix"
            )

        if not hasattr(record, "msgsuffix"):
            record.msgsuffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
                "msgsuffix"
            )

        if not hasattr(record, "module"):
            record.module = get_caller_name()[0]
        if not hasattr(record, "funcName"):
            record.funcName = get_caller_name()[1]

        record.levelname = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get(
            "label"
        )
        formatter = logging.Formatter(self.FORMAT, "%d-%m-%y %H:%M:%S")
        return formatter.format(record)


class EzpylogFormatter(logging.Formatter):
    """A class for formatting logs."""

    FORMAT = f"%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s] %(message)s"

    def format(self, record):
        formatter = logging.Formatter(self.FORMAT, "%d-%m-%y %H:%M:%S")
        return formatter.format(record)


class Logger(object):
    def __init__(
        self,
        name=None,
        min_level: int = logging.INFO,
        logfile: str = None,
        logfile_level=None,
        color_on_console: bool = True,
        stacklevel=2,
        compact=False,
    ):
        """Initialize the logger.
        :param `min_level`: The minimum level of log to be displayed.
        :param `logfile`: The file to log to.
        :param `logfile_level`: The minimum level of log to be written to the logfile.
        :param `color_on_console`: Whether to color the log on the console.
        :param `stacklevel`: The stacklevel to use when logging (disabled with python <3.8).
        """
        if not isinstance(min_level, int):
            raise ValueError("min_level must be a int")
        self._logger: logging.Logger = (
            logging.getLogger() if name is None else logging.getLogger(name)
        )

        if OLD_PYTHON:
            self._logger.findCaller = findCallerPatch

        self._handler = logging.Handler()
        self._handler.setFormatter(EzpylogFormatter())

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(
            EzpylogColoredFormatter(compact=compact)
        ) if color_on_console else self.stream_handler.setFormatter(EzpylogFormatter())
        self._logger.addHandler(self.stream_handler)

        if logfile is not None:
            self._file_handler = logging.FileHandler(
                logfile, mode="a", encoding="utf-8"
            )
            self._file_handler.setFormatter(EzpylogFormatter())
            self._file_handler.setLevel(
                logfile_level if logfile_level is not None else min_level
            )
            self._logger.addHandler(self._file_handler)

        self._logger.setLevel(min_level)
        self.stacklevel = stacklevel

    def set_level(self, level: int):
        """Set the minimum level of log to be displayed.
        :param `level`: The minimum level of log to be displayed.
        """
        self._logger.setLevel(level)

    def log(self, msg, level: int = logging.INFO, stacklevel_offset=0):
        """Log a message.
        :param `msg`: The message to be logged.
        :param `level`: The level of the message.
        :param `context`: The context of the message.
        """

        if not isinstance(msg, SUPPORTED_TYPES):
            try:
                text = str(msg)
            except:
                raise TypeError(
                    f"msg must be {SUPPORTED_TYPES.join(', ')} or convertable to a string"
                )
        elif isinstance(msg, dict):
            text = dict_to_str(msg)
        else:
            text = msg
        splitted = text.split("\n")
        space = ONE_LINE_CHAR
        space += MULTI_LINE_CHAR if len(splitted)>1 else "" 
        for i,line in enumerate(splitted):
            if OLD_PYTHON:
                self._logger.log(level, f"{space}{line}")
            else:
                self._logger.log(
                    level,
                    f"{space}{line}",
                    stacklevel=self.stacklevel + stacklevel_offset,
                )

    def getLogger(self):
        return self._logger

    def debug(self, msg=""):
        self.log(msg, logging.DEBUG, stacklevel_offset=1)

    def info(self, msg=""):
        self.log(msg, logging.INFO, stacklevel_offset=1)

    def warning(self, msg=""):
        self.log(msg, logging.WARNING, stacklevel_offset=1)

    def error(self, msg=""):
        self.log(msg, logging.ERROR, stacklevel_offset=1)

    def critical(self, msg=""):
        self.log(msg, logging.CRITICAL, stacklevel_offset=1)

    def close(self):
        for handler in self._logger.handlers:
            handler.close()
            self._logger.removeHandler(handler)

    def __del__(self):
        self.close()


def loggerdemo():
    print()

    a = 1234567

    logger = Logger("TestLogger", min_level=logging.DEBUG, logfile="log.txt",compact=True)
    logger.log("Debug message\non\nmultiple\nline", logging.DEBUG)
    logger.log("Info message")
    logger.log("Warning message", logging.WARNING)
    logger.log(f"Error message {a}", logging.ERROR)
    logger.log("Critical message", logging.CRITICAL)
    logger.warning({})

    print("", flush=True)

    logger2 = Logger(
        __name__, logging.WARNING, color_on_console=False, logfile="log.txt"
    )
    logger2.log("Debug message", logging.DEBUG)
    logger2.log("Info message", logging.INFO)
    logger2.log("Warning message", logging.WARNING)
    logger2.log(f"Error message {a}", logging.ERROR)
    logger2.log("Critical message", logging.CRITICAL)
    print()


if __name__ == "__main__":
    loggerdemo()

# Copyright 2022, JRodez <jeremierodez@outlook.com>

import sys
import enum
from datetime import datetime
from abc import ABC


class LogLevel(enum.Enum):
    """ Enum for log levels """
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class colorbase(ABC):
    DEBUG = ''
    INFO = ''
    WARNING = ''
    ERROR = ''
    CRITICAL = ''
    CRITICALMSG = ''
    CONTEXT = ''
    ENDC = ''


class bcolors(colorbase):
    DEBUG = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[1m\033[91m'
    CRITICALMSG = '\033[4m'
    CONTEXT = '\033[96m'
    ENDC = '\033[0m'


class noncolor(colorbase):
    DEBUG = ''
    INFO = ''
    WARNING = ''
    ERROR = ''
    CRITICAL = ''
    CRITICALMSG = ''
    CONTEXT = ''
    ENDC = ''


class Logger:
    def __init__(self,  min_level: LogLevel = LogLevel.INFO, contextprefix="", logfile="stdout", errorlogfile="stderr"):
        """ Initialize the logger. 
        :param `min_level`: The minimum level of log to be displayed.
        :param `contextprefix`: The prefix to be added to the context.
        :param `logfile`: The file to log to.
        :param `errorlogfile`: The file to log errors to.
        """

        if not isinstance(min_level, LogLevel):
            raise ValueError('min_level must be a LogLevel')
        self.min_level: LogLevel = min_level

        self._contextprefix = ""
        if contextprefix != "":
            self._contextprefix = contextprefix

        if logfile == "stdout":
            self._file = sys.stdout
        elif isinstance(errorlogfile, str):
            self._file = open(logfile, 'w')
        else:
            self._file = logfile

        if errorlogfile != logfile:
            if errorlogfile == "stderr":
                self._errorfile = sys.stderr
            elif isinstance(errorlogfile, str):
                self._errorfile = open(errorlogfile, 'w')
            else:
                self._errorfile = errorlogfile
        else:
            self._errorfile = self._file

        self._colormanager: colorbase = bcolors if self._file in [
            sys.stdout, sys.stderr] and self._errorfile in [sys.stdout, sys.stderr] else noncolor

    def log(self, msg, level: LogLevel = LogLevel.INFO, context=""):
        """ Log a message. 
        :param `msg`: The message to be logged.
        :param `level`: The level of the message.
        :param `context`: The context of the message.
        """
        if type(msg) is not str:
            try:
                msg = str(msg)
            except:
                raise ValueError(
                    'msg must be a string or convertable to a string')

        if level.value >= self.min_level.value:
            sep = "." if self._contextprefix != "" and context != "" else ""
            contextprefix = self._contextprefix if self._contextprefix != "" else ""
            context = context if context != "" else ""
            contextstr = (f"{contextprefix}{sep}{context}")
            contextmsg = f"{self._colormanager.CONTEXT}[{contextstr}]{self._colormanager.ENDC}" if contextstr != "" else ""

            now = datetime.now().strftime("%H:%M:%S")
            splitted = msg.split("\n")
            for line in splitted:
                space = '> ' if len(splitted) > 1 else ''

                if level == LogLevel.CRITICAL:
                    self._errorfile.write(
                        f"{now} | {self._colormanager.CRITICAL}[CRITICAL]{self._colormanager.ENDC} {contextmsg} {self._colormanager.ERROR}{space}{line}{self._colormanager.ENDC}\n")

                elif level == LogLevel.ERROR:
                    self._errorfile.write(
                        f"{now} | {self._colormanager.ERROR}[ERROR]{self._colormanager.ENDC} {contextmsg} {space}{line}\n")

                elif level == LogLevel.WARNING:
                    self._file.write(
                        f"{now} | {self._colormanager.WARNING}[WARNING]{self._colormanager.ENDC} {contextmsg} {space}{line}\n")

                elif level == LogLevel.INFO:
                    self._file.write(
                        f"{now} | {self._colormanager.INFO}[INFO]{self._colormanager.ENDC} {contextmsg} {space}{line}\n")

                elif level == LogLevel.DEBUG:
                    self._file.write(
                        f"{now} | {self._colormanager.DEBUG}[DEBUG]{self._colormanager.ENDC} {contextmsg} {space}{line}\n")

                else:
                    raise Exception('Unknown log level')
            self._file.flush()

    def debug(self, msg, context=""):
        self.log(msg, LogLevel.DEBUG, context)

    def info(self, msg, context=""):
        self.log(msg, LogLevel.INFO, context)

    def warning(self, msg, context=""):
        self.log(msg, LogLevel.WARNING, context)

    def error(self, msg, context=""):
        self.log(msg, LogLevel.ERROR, context)

    def critical(self, msg, context=""):
        self.log(msg, LogLevel.CRITICAL, context)

    def close(self):
        if self._file != self._errorfile:
            self._errorfile.close()
        self._file.close()

    def __del__(self):
        self.close()


def loggerdemo():
    print()

    a = 1234567

    logger = Logger(LogLevel.DEBUG)
    logger.log("Debug message\non\nmultiple\nline", LogLevel.DEBUG, "context")
    logger.log("Info message")
    logger.log("Warning message", LogLevel.WARNING, "context")
    logger.log(f"Error message {a}", LogLevel.ERROR, "context")
    logger.log("Critical message", LogLevel.CRITICAL, "context")

    print()

    logger2 = Logger(LogLevel.WARNING, "__main__")
    logger2.log("Debug message", LogLevel.DEBUG, "subcontextA()")
    logger2.log("Info message", LogLevel.INFO, "subcontextB()")
    logger2.log("Warning message", LogLevel.WARNING, "subcontextA()")
    logger2.log(f"Error message {a}", LogLevel.ERROR, "subcontextB()")
    logger2.log("Critical message", LogLevel.CRITICAL)

    print()


if __name__ == "__main__":
    loggerdemo()

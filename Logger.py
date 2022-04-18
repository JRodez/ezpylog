# MIT Licence :
# https://opensource.org/licenses/MIT

###########################################################################################################################
#                                                                                                                         #
# Copyright 2022 Jérémie RODEZ                                                                                            #
#                                                                                                                         #
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated            #
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation         #
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and        #
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:                      #
#                                                                                                                         #
# The above copyright notice and this permission notice shall be included in all copies or substantial portions           #
# of the Software.                                                                                                        #
#                                                                                                                         #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO        #
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE          #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,     #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE          #
# SOFTWARE.                                                                                                               #
#                                                                                                                         #
###########################################################################################################################



import sys
import enum
from datetime import datetime


class LogLevel(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class bcolors:
    DEBUG = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[1m\033[91m'
    CRITICALMSG = '\033[4m'
    CONTEXT = '\033[96m'
    ENDC = '\033[0m'


class noncolor:
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

        self.min_level = min_level

       
        self.contextprefix = ""
        if contextprefix != "":
            self.contextprefix = contextprefix

        if logfile == "stdout":
            self.file = sys.stdout
        elif isinstance(errorlogfile, str):
            self.file = open(logfile, 'w')
        else:
            self.file = logfile

        if errorlogfile != logfile:
            if errorlogfile == "stderr":
                self.errorfile = sys.stderr
            elif isinstance(errorlogfile, str):
                self.errorfile = open(errorlogfile, 'w')
            else:
                self.errorfile = errorlogfile
        else:
            self.errorfile = self.file

        self.colormanager = bcolors if self.file in [
            sys.stdout, sys.stderr] and self.errorfile in [sys.stdout, sys.stderr] else noncolor

    def log(self, msg, level: LogLevel = LogLevel.INFO, context=""):
        if level.value >= self.min_level.value:
            sep = "." if self.contextprefix != "" and context != "" else ""
            contextprefix = self.contextprefix if self.contextprefix != "" else ""
            context = context if context != "" else ""
            contextstr = (f"{contextprefix}{sep}{context}")
            contextmsg = f"{self.colormanager.CONTEXT}[from {contextstr}]{self.colormanager.ENDC}" if contextstr != "" else ""

            now = datetime.now().strftime("%H:%M:%S")

            if level == LogLevel.CRITICAL:
                self.errorfile.write(
                    f"{now} | {self.colormanager.CRITICAL}[CRITICAL]{self.colormanager.ENDC} {contextmsg} {self.colormanager.ERROR}{msg}{self.colormanager.ENDC}\n")

            elif level == LogLevel.ERROR:
                self.errorfile.write(
                    f"{now} | {self.colormanager.ERROR}[ERROR]   {self.colormanager.ENDC} {contextmsg} {msg}\n")

            elif level == LogLevel.WARNING:
                self.file.write(
                    f"{now} | {self.colormanager.WARNING}[WARNING] {self.colormanager.ENDC} {contextmsg} {msg}\n")

            elif level == LogLevel.INFO:
                self.file.write(
                    f"{now} | {self.colormanager.INFO}[INFO]    {self.colormanager.ENDC} {contextmsg} {msg}\n")

            elif level == LogLevel.DEBUG:
                self.file.write(
                    f"{now} | {self.colormanager.DEBUG}[DEBUG]   {self.colormanager.ENDC} {contextmsg} {msg}\n")

            else:
                raise Exception('Unknown log level')
            self.file.flush()

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
        if self.file != self.errorfile:
            self.errorfile.close()
        self.file.close()

    def __del__(self):
        self.close()




def loggerdemo():
    print()

    a = 1234567

    logger = Logger(LogLevel.DEBUG)
    logger.log("Debug message", LogLevel.DEBUG, "context")
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

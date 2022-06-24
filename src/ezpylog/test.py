import logging


class bcolors:
    NEUTRAL = "\033[97m"
    DEBUG = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[1m\033[91m'
    CRITICALMSG = '\033[4m\033[91m'
    CONTEXT = '\033[96m'
    ENDC = '\033[0m'


class ColorLogFormatter(logging.Formatter):
    """A class for formatting colored logs."""

    LOG_LEVEL_COLOR = {
        "DEBUG": {'lvlprefix': bcolors.DEBUG, 'lvlsuffix': bcolors.ENDC, 'msgprefix': "", 'msgsuffix':  bcolors.ENDC},
        "INFO": {'lvlprefix': bcolors.INFO, 'lvlsuffix': bcolors.ENDC, 'msgprefix': "", 'msgsuffix':  bcolors.ENDC},
        "WARNING": {'lvlprefix': bcolors.WARNING, 'lvlsuffix': bcolors.ENDC, 'msgprefix': "", 'msgsuffix':  bcolors.ENDC},
        "ERROR": {'lvlprefix': bcolors.ERROR, 'lvlsuffix': bcolors.ENDC, 'msgprefix': bcolors.ERROR, 'msgsuffix':  bcolors.ENDC},
        "CRITICAL": {'lvlprefix': bcolors.CRITICAL, 'lvlsuffix': bcolors.ENDC, 'msgprefix': bcolors.CRITICALMSG, 'msgsuffix':  bcolors.ENDC},
    }
    FORMAT = f"%(asctime)s | %(lvlprefix)s[%(levelname)s]%(lvlsuffix)s {bcolors.CONTEXT}[%(module)s.%(funcName)s]{bcolors.ENDC} %(msgprefix)s%(message)s%(msgsuffix)s"

    def format(self, record):

        self.datefmt = '%Y-%m-%d %H:%M:%S'
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


class machin():
    def entent(self):
        logger = logging.getLogger('bobcat')
        logger.setLevel('DEBUG')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(ColorLogFormatter())
        logger.addHandler(stream_handler)

        logger.debug("This is debug")
        logger.info("This is info")
        logger.info("This is a green info", extra={
                    'msgprefix': bcolors.INFO})
        logger.warning("This is warning")
        logger.error("This is error")
        logger.critical("This is critical")


m = machin()
m.entent()

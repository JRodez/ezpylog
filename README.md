# Welcome
ezpylog is a minimalistic and easy to use python logger
## Installation
Using pip :
 - directly from command line with : `pip install ezpylog` 
 - manually by [downloading ezpylog](https://github.com/JRodez/ezpylog/releases) and install it with `pip install ezpylog-X.X.tar.gz`

## How to use ?
### Import :
```python
from ezpylog import Logger, LogLevel
```

### Logging Levels :
The level can be as following :
```python
LogLevel.DEBUG
LogLevel.INFO
LogLevel.WARNING
LogLevel.ERROR
LogLevel.CRITICAL
```

### Initialisation :
```python
logger = Logger(name=None,  
				min_level: int = logging.WARNING, 
				logfile: str = None, 
				logfile_level=None, 
				color_on_console: bool = True)
```
- `name` is the name of the logger. If not set, the name of the module will be used.
- `min_level` is a `LogLevel` enum and filters log messages on the console (ex : `WARNING` will not print `INFO` messages). Default is `WARNING`.
- `context` is the logging context, you can use `"main()"` if you use it in `__main__` for example. Default is `""`.
- `logfile` is the name of your optional log file for `DEBUG`,`INFO` and `DEBUG` messages. Default is `None` (no log file).
- `logfile_level` is a `LogLevel` enum and filters log messages in the log file (ex : `WARNING` will not print `INFO` messages). Default is `WARNING`.
- `color_on_console` is a boolean to enable or disable color on the console. Default is `True`.

### logging : 
```python
logger.log(msg)
# or
logger.log(msg, level)
```
with default `level = LogLevel.INFO`.

You can call the loglevel corresonding function too :
```python
logger.debug(msg)
logger.info(msg)
logger.warning(msg)
logger.error(msg)
logger.critical(msg)
```

## Example :
You can find this exemple by calling `Logger.loggerdemo()`

```python
from ezpylog import Logger, LogLevel

a = 1234567

logger = Logger(LogLevel.DEBUG)
logger.log("Debug message", LogLevel.DEBUG, "context")
logger.log("Info message")
logger.log("Warning message", LogLevel.WARNING, "context")
logger.log(f"Error message {a}", LogLevel.ERROR, "context")
logger.log("Critical message", LogLevel.CRITICAL, "context")

logger2 = Logger(LogLevel.WARNING, "__main__")
logger2.log("Debug message", LogLevel.DEBUG, "subcontextA()")
logger2.log("Info message", LogLevel.INFO, "subcontextB()")
logger2.log("Warning message", LogLevel.WARNING, "subcontextA()")
logger2.log(f"Error message {a}", LogLevel.ERROR, "subcontextB()")
logger2.log("Critical message", LogLevel.CRITICAL)
```	

prints the following : 

![image](https://user-images.githubusercontent.com/80471345/163835427-f5b3306f-9ebe-46d4-9da6-1e5413f8af0e.png)

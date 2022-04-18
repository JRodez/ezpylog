# ezpylog
Minimalistic and easy to use python logger

## How to use ?
### Import :
Import logger.py the way you want, personnaly I do : 

```python
from logger import Logger, LogLevel
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
logger = Logger(min_level = LogLevel.INFO, context = "", inf_file="stdout", error_file="stderr")
```

- `min_level` is a `LogLevel` enum and filters log messages on the console (ex : `WARNING` will not print `INFO` messages). Default is `INFO`
- `context` is the logging context, you can use `"main()"` if you use it in `__main__` for example. Default is `""`
- `inf_file` is the name of your output file  for `DEBUG`,`INFO` and `DEBUG` messages. Default is `stdout`
- `error_file` is the name of your output file  for `ERROR` and `CRITICAL` messages. Default is `stderr`

### logging : 
```python
logger.log(msg)
# or
logger.log(msg, level)
# or
logger.log(msg, level, subcontext)
```
with default `level = LogLevel.INFO` and `subcontext = ""`

### Example :
You can find this exemple by calling `Logger.loggerdemo()`

```python
from logger import Logger, LogLevel

a = 1234567

logger = Logger()
logger.log("Debug message", LogLevel.DEBUG, "context")
logger.log("Info message", LogLevel.INFO, "context")
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

![image](https://user-images.githubusercontent.com/80471345/163833341-8036c41f-333b-4fc9-987d-3475a509396a.png)

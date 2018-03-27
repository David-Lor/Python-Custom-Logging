# Python-Custom-Logging
My custom Logging addon for Python native logging library, using SQLite and my [custom SQLite-DBManager](https://github.com/EnforcerZhukov/Python-SQLite-DBManager)

## Example of use

```python
from Logging import logging, create_logger

mylog = create_logger(
    name="PyBuses",
    db_name="Databases/VigoBusLog.sqlite",
    db_level=logging.DEBUG,
    print_level=logging.DEBUG
)

mylog.debug("This is a common debug msg")
mylog.info("This is just info")
mylog.error("This is an ERROR!")
```

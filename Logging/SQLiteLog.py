
#Native libraries
import logging
import time
#Own modules
from datetime import datetime
from Databases import Database

# We store opened databases on the following dict
# This avoids generating multiple Database objects for the same DB,
#   when we create a logger with the same DB name as another logger
databases = dict() #{databaseName : databaseObject}

class DatabaseLog(logging.Handler):
    def __init__(self, db_name, datetime_format="%y-%m-%d %H:%M:%S"):
        """
        :param db_name: Name (relative route) of the database to be created/used
        :param datetime_format: Format of Datetime fields on database (default: %y-%m-%d %H:%M:%S)
        """
        logging.Handler.__init__(self)
        if db_name in databases: #Don't create new SQLite object/connection if it's already running
            self.db = databases[db_name]
        else:
            self.db = Database(db_name)
            self.db.write("""CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                logger TEXT NOT NULL,
                level INTEGER NOT NULL,
                function TEXT NOT NULL,
                text TEXT NOT NULL
            )""")
            databases[db_name] = self.db
        self.datetime_format = datetime_format

    def emit(self, record):
        """This method will be called by logging when a new log is created.
        :param record: logging record (objects used by logging module)
        """
        self.db.write("INSERT INTO logs (datetime, logger, level, function, text) VALUES (?,?,?,?,?)", (
            datetime.fromtimestamp(record.created).strftime(self.datetime_format), #datetime
            record.name, #logger name
            record.levelname, #level
            record.funcName, #function
            record.msg, #text
        ))


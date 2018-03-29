
#Native libraries
import logging
import threading
import atexit
from datetime import datetime
#Own modules
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
        self.datetime_format = datetime_format
        #Commit service thread
        self._commit_service_stopEvent = threading.Event()
        self._commit_service_thread = None
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
            #Commit service thread
            self.start_commit_service()
            @atexit.register
            def atexit_f():
                self.stop_commit_service()
                self.db.commit()

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
        ), commit=False)
    
    def _commit_service(self, stopEvent, frequency):
        while not stopEvent.isSet():
            self.db.commit()
            stopEvent.wait(timeout=frequency)
    
    def start_commit_service(self, frequency=5):
        self._commit_service_stopEvent.clear()
        self._commit_service_thread = threading.Thread(
            target=self._commit_service,
            args=(self._commit_service_stopEvent, frequency),
            daemon=True
        )
        self._commit_service_thread.start()
    
    def stop_commit_service(self):
        if self.is_commit_service_running():
            self._commit_service_stopEvent.set()

    def is_commit_service_running(self):
        if self._commit_service_thread is None:
            return False
        return self._commit_service_thread.is_alive()



#Native libraries
import logging
#import atexit
#Own modules
from .SQLiteLog import DatabaseLog

loggers = list()

# @atexit.register
# def atexit_f():
#     for logger in loggers:
#         logger.shutdown()

def create_logger(name, db_name=None, level=logging.DEBUG, db_level=logging.INFO, print_level=None, print_format="[%(levelname)s][%(asctime)s]@%(name)s - %(message)s", print_datetime_format="%m/%d-%H:%M:%S"):
    """
    :param name: Log name
    :param db_name: Name (relative route) of the SQLite database (default=None -> db_name=name+".sqlite")
    :param level: Level of this logger (default=DEBUG a.k.a. log everything)
    :param db_level: Level of logs that will be stored in DB (default=INFO; None=Store nothing in DB)
    :param print_level: Level of logs that will be printed on local console (default=None a.k.a. print nothing in screen)
    :param print_format: Console print format (default: "[%(levelname)s][%(asctime)s]@%(name)s - %(message)s")
    :param print_datetime_format: Console print datetime format  (default: "%m/%d-%H:%M:%S")
    """
    #Create logger object and set logger level
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    #Add SQLite Handler
    if db_level is not None:
        if db_name is None:
            db_name = name + ".sqlite"
        db_handler = DatabaseLog(db_name)
        db_handler.setLevel(db_level)
        logger.addHandler(db_handler)

    #Add print to console handler (StreamHandler)
    if print_level is not None:
        print_handler = logging.StreamHandler()
        print_handler.setLevel(print_level)
        print_handler.setFormatter(
            logging.Formatter(
                fmt=print_format,
                datefmt=print_datetime_format
            )
        )
        logger.addHandler(print_handler)

    #Append logger to local loggers list and return object
    loggers.append(logger)
    return logger

def get_logger(name):
    try:
        return next(l for l in loggers if l.name == name)
    except StopIteration:
        return None

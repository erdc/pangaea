#
# Originally from quest python library
# Adapted for pangaea
#
# License: BSD 3-Clause

import logging
import appdirs
import os

from . import version()

logger = logging.getLogger('pangaea')
null_handler = logging.NullHandler()
logger.addHandler(null_handler)
logger.propagate = False

default_log_dir = appdirs.user_log_dir('pangaea', 'logs')
default_log_file = os.path.join(default_log_dir, 'pangaea.log')


def log_to_console(status=True, level=None):
    """Log events to  the console.

    Args:
        status (bool, Optional, Default=True)
            whether logging to console should be turned on(True) or off(False)
        level (string, Optional, Default=None) :
            level of logging; whichever level is chosen all higher levels will be logged.
            See: https://docs.python.org/2/library/logging.html#levels
      """

    if status:
        if level is not None:
            logger.setLevel(level)

        console_handler = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter('%(levelname)s-%(name)s: %(message)s')
        # add formatter to handler
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info("pangaea {0}".format(version()))

    else:
        for h in logger.handlers:
            if type(h).__name__ == 'StreamHandler':
                logger.removeHandler(h)



def log_to_file(status=True, filename=default_log_file, level=None):
    """Log events to a file.

    Args:
        status (bool, Optional, Default=True)
            whether logging to file should be turned on(True) or off(False)
        filename (string, Optional, Default=None) :
            path of file to log to
        level (string, Optional, Default=None) :
            level of logging; whichever level is chosen all higher levels will be logged.
            See: https://docs.python.org/2/library/logging.html#levels
      """

    if status:
        if level is not None:
            logger.setLevel(level)

        try:
            os.mkdir(os.path.dirname(filename))
        except OSError:
            pass

        file_handler = logging.FileHandler(filename)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s-%(name)s: %(message)s')
        # add formatter to handler
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info("pangaea {0}".format(version()))

    else:
        for h in logger.handlers:
            if type(h).__name__ == 'FileHandler':
                logger.removeHandler(h)
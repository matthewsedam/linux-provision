# util.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import datetime
import logging
import os
import platform
import sys
from config import Config

LOG_FILE_NAME = ('linux_security_provision-' +
                 datetime.datetime.now().strftime('%m-%d-%y') +
                 '.log')


# Does general setup
def setup():
    setup_logging()
    if platform.system() != 'Linux':
        logging.error('This script can only be run on Linux')
        sys.exit(1)
    if os.geteuid() != 0:
        logging.error('You must run this script as root! Use sudo.')
        sys.exit(1)

    config = Config.get_config()
    logging.info('Setup successful.')
    return config


# Sets up logging to write to file and to stdout
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # setup log to file
    file_formatter = logging.Formatter('[%(asctime)s]: %(levelname)s: ' +
                                       '%(message)s')
    file_handler = logging.FileHandler(LOG_FILE_NAME)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # setup logging to console
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

# util.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import logging
import subprocess

BASE_HOME_DIR = '/home/'
SSHD_CONFIG_FILE_NAME = '/etc/ssh/sshd_config'


def run_command(command):
    """
    Runs command and returns (the returncode, stdout, stderr) or raises an
    exception if returncode != 0.
    """

    logger = logging.getLogger()
    command_string = ' '.join(command)
    logger.info(f'Start command: {command_string}')

    proc = subprocess.run(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise Exception(f'Error running process: {proc.stdout}: {proc.stderr}')

    logger.info(f'Finish command: {command_string}')
    return (proc.returncode, proc.stdout, proc.stderr)

# util.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import logging
import subprocess

LOGGER = logging.getLogger()


def run_command(command):
    """
    Runs command and returns (the returncode, stdout, stderr) or raises an
    exception if returncode != 0.
    """

    logger = logging.getLogger()
    logger.info(f'Util: Running command: {' '.join(command)}')

    proc = subprocess.run(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(
            f'Error running process: {proc.stdout}: {proc.stderr}')

    return (proc.returncode, proc.stdout, proc.stderr)

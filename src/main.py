# main.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import logging
from setup import setup

# Import modules
from pmodules.ssh_pmod import SSHPMod

MODULES = [SSHPMod()]


def main():
    config = setup()
    logger = logging.getLogger()

    for module in MODULES:
        try:
            module.run()
        except Exception as excp:
            excp_str = str(excp)
            if len(excp_str) > 0:
                excp_str = ': ' + excp_str
            logger.error('Error running module: ' +
                         module.get_name() + excp_str)


if __name__ == '__main__':
    main()

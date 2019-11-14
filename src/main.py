# main.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import logging
from pmodules.ssh_pmod import SSHPMod
from util import setup

MODULES = [SSHPMod()]


def main():
    config = setup()
    logger = logging.getLogger()

    for module in MODULES:
        try:
            module.setup_config(config)
            module.run()
        except Exception as excp:
            excp_str = str(excp)
            logger.error('Error running module: ' +
                         module.get_name() +
                         (': ' + excp_str
                          if len(excp_str) > 0
                          else ''))


if __name__ == '__main__':
    main()

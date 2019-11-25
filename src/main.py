# main.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import logging
from setup import setup

# Import modules
from ssh_pmod import SSHPMod
from user_pmod import UserPMod

MODULES = [UserPMod, SSHPMod]


def main():
    config = setup()
    logger = logging.getLogger()

    modules = [Module(config) for Module in MODULES]
    for module in modules:
        try:
            # module.run()
            pass
        except Exception as excp:
            excp_str = str(excp)
            if len(excp_str) > 0:
                excp_str = ': ' + excp_str
            logger.error('Error running module: ' +
                         module.get_name() + excp_str)


if __name__ == '__main__':
    main()

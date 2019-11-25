# port_scan_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License


import logging
from provisioning_module import ProvisioningModule
from util import run_command


class PortScanPMod(ProvisioningModule):
    """Provisioning module for running a port scan."""

    def __init__(self, config=None):
        pass

    def run(self):
        """
        Runs the provisioning for this module. Does the following.

        1. Run Nmap port scanning on localhost
        """

        logger = logging.getLogger()
        output = run_command(['nmap', '-p0-', 'localhost'])
        logger.info('Nmap output:\n' + output[1])

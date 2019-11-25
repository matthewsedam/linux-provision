# user_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License


from provisioning_module import ProvisioningModule
from util import run_command


class UserPMod(ProvisioningModule):
    """Provisioning module for user configuration."""

    def __init__(self, config=None):
        pass

    def run(self):
        """
        Runs the provisioning for this module. Does the following.

        1. Delete the root password
        """

        run_command(['passwd', '-dl', 'root'])

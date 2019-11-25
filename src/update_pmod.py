# update_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License


from provisioning_module import ProvisioningModule
from util import run_command


class UpdatePMod(ProvisioningModule):
    """Provisioning module for update configuration."""

    def __init__(self, config=None):
        pass

    def run(self):
        """
        Runs the provisioning for this module. Does the following.

        1. Updates packages
        2. Configures automatic updates.
        3. Does full update.
        """

        run_command(['apt-get', 'update'])
        run_command(['apt-get', 'install', '-y', 'unattended-upgrades'])
        run_command(['apt-get', 'upgrade', '-y'])

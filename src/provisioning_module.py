# provisioning_module.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License


class ProvisioningModule:
    # Abstract base class for all modules
    def __init__(self):
        raise NotImplementedError

    def setup_config(self, config):
        # Should ensure all needed keys are in config by
        # prompting the user for the missing data.
        # Note: This method will be called by the
        # main configuration setup and must be implemented.
        raise NotImplementedError

    def run(self):
        # Runs the provisioning for this module.
        raise NotImplementedError

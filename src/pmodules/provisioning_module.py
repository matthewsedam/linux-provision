# provisioning_module.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License


class ProvisioningModule:
    """Abstract base class for all modules"""

    def __init__(self, config=None):
        """
        Ensures all needed keys are in config by
        prompting the user for the missing data and
        store needed information internally.
        """

        raise NotImplementedError

    def get_name(self):
        """Returns the name of the module."""

        raise NotImplementedError

    def run(self):
        """Runs the provisioning for this module."""

        raise NotImplementedError

# ssh_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import logging
import os
from functools import reduce


class SSHPMod(ProvisioningModule):
    # Provisioning module for SSH configuration
    def __init__(self):
        self.logger = logging.getLogger()

    def setup_config(self, config):
        # Should ensure all needed keys are in config by
        # prompting the user for the missing data.
        # Note: This method will be called by the
        # main configuration setup and must be implemented.

        # TODO: FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        needed_keys = []
        is_okay = True

        # list of users to check if they have an outgoing key
        if 'users' not in config:
            needed_keys.append('users')
        else:
            users = config['users']
            if not isinstance(users, list) or len(users) == 0:
                self.logger.error('SSHPMod: Key "users" should be an array of ' +
                                  'length > 0')
                is_okay = False
            else:
                for user in users:
                    if (not isinstance(user, dict) or
                        'deleteAllSSHKeys' not in user or
                        not isinstance(user['deleteAllSSHKeys'], bool) or
                        'authorizedKeys' not in user or
                        not isinstance(user['authorizedKeys'], list) or
                        not all(map(lambda akey: isinstance(akey, str) and
                                                 len(akey) > 0, user['authorized_keys'])):
                        self.logger.error('SSHPMod: Key "users" array must contain ' +
                                          'user objects with the following key(s): ' +
                                          '"deleteAllSSHKeys" (boolean), ' +
                                          '"authorizedKeys" (array of non-empty strings)')
                        is_okay = False
                        break

        if 'base_home_dir' not in config:
            needed_keys.append('base_home_dir')
        else:
            base_home_dir = config['base_home_dir']
            if not isinstance(base_home_dir, str) or len(base_home_dir) == 0:
                self.logger.error('SSHPMod: Key "base_home_dir" should be a ' +
                                  'non-empty string')
                is_okay = False

        needed_keys.sort()
        return (needed_keys, is_okay and len(needed_keys) == 0)

    def run(self):
        # Runs the provisioning for this module.

        # 1. For every user, do the following:
        #   1. Create ~/.ssh folder if needed
        #   2. Set required permissions and ownership on ~/.ssh folder
        #   3. Delete ~/.ssh/known_hosts
        #   4. Delete ~/.ssh/authorized_keys
        #   5. Create ~/.ssh/authorized_keys with required permissions and
        #      ownership
        #   6. For each authorized key, add it to ~/.ssh/authorized_keys
        #   7. Remove all ~/.ssh/id_* if user["deleteAllSSHKeys"] is true
        # 2. Set "PasswordAuthentication no" in /etc/ssh/sshd_config and
        #    restart the ssh service

        raise NotImplementedError  # TODO

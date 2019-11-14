# ssh_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import json
import logging
import os
from functools import reduce
from .provisioning_module import ProvisioningModule


class SSHPMod(ProvisioningModule):
    # Provisioning module for SSH configuration
    def __init__(self):
        self.logger = logging.getLogger()
        self.users = None

    def get_name(self):
        # Returns the name of the module
        return 'SSHPMod'

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

    def setup_config(self, config):
        # Should ensure all needed keys are in config by
        # prompting the user for the missing data.
        # Note: This method will be called by the
        # main configuration setup and must be implemented.

        def _check_user(user):
            return (isinstance(user, dict) and
                    'username' in user and
                    isinstance(user['username'], str) and
                    len(user['username']) > 0 and
                    user['username'] != 'root' and
                    'deleteAllSSHKeys' in user and
                    isinstance(user['deleteAllSSHKeys'], bool) and
                    'authorizedKeys' in user and
                    isinstance(user['authorizedKeys'], list) and
                    all(map(lambda akey: isinstance(akey, str) and len(akey) > 0,
                            user['authorized_keys'])) and
                    'home_dir' in user and
                    os.path.isdir(user['home_dir']))

        def _get_user(user=None):
            new_user = {}
            if user:
                print('SSHPMod: Replacing bad user:', user)

            new_user['username'] = ''
            while len(new_user['username']) == 0 or new_user['username'] == 'root':
                ipt = input(
                    'SSHPMod: User: username [NOT "root"]: ').strip().lower()
                new_user['username'] = ipt

            ipt = input(
                'SSHPMod: User: deleteAllSSHKeys [true]: ').strip().lower()
            new_user['deleteAllSSHKeys'] = ipt != 'false'

            auth_key = None
            new_user['authorized_keys'] = []
            while auth_key is None or len(auth_key) != 0:
                if auth_key:
                    new_user['authorized_keys'].append(auth_key)

                auth_key = input(
                    'SSHPMod: User: authorized_key [ENTER when done]: ')

            new_user['home_dir'] = ''
            while not os.path.isdir(new_user['home_dir']):
                new_user['home_dir'] = input('SSHPMod: User: home_dir: ')

            return new_user

        users = (config['users']
                 if 'users' in config and isinstance(config['users'], list) else [])
        while len(users) == 0:
            for i, user in enumerate(users):
                if not _check_user(user):
                    users[i] = _get_user(user)

            if len(users) == 0:
                users = [_get_user()]
        self.users = users

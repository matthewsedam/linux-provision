# ssh_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import json
import logging
import os
from functools import reduce
from .provisioning_module import ProvisioningModule


BASE_HOME_DIR = '/home/'


class SSHPMod(ProvisioningModule):
    """Provisioning module for SSH configuration."""

    def __init__(self, config=None):
        """
        Ensures all needed keys are in config by
        prompting the user for the missing data and
        store needed information internally.
        """

        self.logger = logging.getLogger()
        self.users = []
        if config and 'users' in config and isinstance(config['users'], list):
            self.users = config['users']

        while (len(self.users) == 0 or
               input('SSHPMod: Setup another user? [y/n]: ').strip().lower() == 'y'):
            new_users = []
            for i, user in enumerate(self.users):
                user_is_good = self._check_user(user)
                user_unique_properties = all(
                    map(lambda usr: user['username'] != usr['username'], self.users[:i]))

                if user_is_good and user_unique_properties:
                    new_users.append(user)
                elif user_unique_properties:
                    self.users.append(self._get_user(user))

            self.users = new_users
            self.users.append(self._get_user())

    def _check_user(self, user):
        """Returns true if a user is of the appropriate format."""

        return (isinstance(user, dict) and
                'username' in user and
                isinstance(user['username'], str) and
                len(user['username']) > 0 and
                user['username'] != 'root' and
                user['username'].isalpha() and
                'deleteAllSSHKeys' in user and
                isinstance(user['deleteAllSSHKeys'], bool) and
                'authorizedKeys' in user and
                isinstance(user['authorizedKeys'], list) and
                len(user['authorizedKeys']) > 0 and
                all(map(lambda akey: isinstance(akey, str) and len(akey) > 0,
                        user['authorizedKeys'])) and
                os.path.isdir(BASE_HOME_DIR + user['username']))

    def _get_user(self, user=None):
        """Gets a new user from the user and returns it."""

        new_user = {}
        if user:
            logging.info('SSHPMod: Replacing bad user:', user)

        new_user['username'] = ''
        while (len(new_user['username']) == 0 or
               new_user['username'] == 'root' or
               not new_user['username'].isalpha() or
               any(map(lambda user: user['username'] == new_user['username'],
                       self.users)) or
               not os.path.isdir(BASE_HOME_DIR + new_user['username'])):
            ipt = input('SSHPMod: User: username [NOT "root" or previous, ' +
                        '/home/$username exists, alpha char only]: ')
            ipt = ipt.strip().lower()
            new_user['username'] = ipt
        new_user['homeDir'] = BASE_HOME_DIR + new_user['username']

        ipt = input('SSHPMod: User: deleteAllSSHKeys [true]: ')
        ipt = ipt.strip().lower()
        new_user['deleteAllSSHKeys'] = ipt != 'false'

        new_user['authorizedKeys'] = []
        while len(new_user['authorizedKeys']) == 0:
            auth_key = None
            while auth_key is None or len(auth_key) > 0:
                if auth_key:
                    new_user['authorizedKeys'].append(auth_key)

                auth_key = input('SSHPMod: User: authorizedKey ' +
                                 '[ENTER when done]: ')

        return new_user

    def get_name(self):
        """Returns the name of the module."""

        return 'SSHPMod'

    def run(self):
        """Runs the provisioning for this module. Does the following.

           1. For every user, do the following:
              1. Create ~/.ssh folder if needed
              2. Set required permissions and ownership on ~/.ssh folder
              3. Delete ~/.ssh/known_hosts
              4. Delete ~/.ssh/authorizedKeys
              5. Create ~/.ssh/authorizedKeys with required permissions and
                 ownership
              6. For each authorized key, add it to ~/.ssh/authorizedKeys
              7. Remove all ~/.ssh/id_* if user["deleteAllSSHKeys"] is true
           2. Set "PasswordAuthentication no" in /etc/ssh/sshd_config and
              restart the ssh service
        """

        raise NotImplementedError  # TODO

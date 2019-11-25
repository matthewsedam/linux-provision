# ssh_pmod.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import json
import logging
import os
from functools import reduce
from provisioning_module import ProvisioningModule
from util import run_command


BASE_HOME_DIR = '/home/'
SSHD_CONFIG_FILE_NAME = '/etc/ssh/sshd_config'


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

    def _update_sshd_config(self):
        """
        Updates SSHD_CONFIG_FILE_NAME to contain 'PasswordAuthentication no'.
        """

        sshd_config = None
        with open(SSHD_CONFIG_FILE_NAME) as file:
            sshd_config = file.read().strip().split('\n')

        new_sshd_config = []
        found_password_auth = False
        for line in sshd_config:
            if (not found_password_auth and
                'passwordauthentication' in line.lower() and
                    line.strip()[0] != '#'):
                new_sshd_config.append('PasswordAuthentication no')
                found_password_auth = True
            else:
                new_sshd_config.append(line)

        if not found_password_auth:
            new_sshd_config.append('PasswordAuthentication no')

        with open(SSHD_CONFIG_FILE_NAME, 'w') as file:
            file.write('\n'.join(new_sshd_config))

    def get_name(self):
        """Returns the name of the module."""

        return 'SSHPMod'

    def run(self):
        """Runs the provisioning for this module. Does the following.

           1. For every user, do the following:
              1. Create ~/.ssh folder if needed
              2. Set required permissions and ownership on ~/.ssh folder - 700
              3. Delete ~/.ssh/authorized_keys
              4. Delete ~/.ssh/known_hosts
              5. Create ~/.ssh/authorized_keys with required permissions and
                 ownership - 600
              6. For each authorized key, add it to ~/.ssh/authorized_keys
              7. Remove all ~/.ssh/id_* if user["deleteAllSSHKeys"] is true
              8. If user["deleteAllSSHKeys"] is false, set all private keys
                 to have permissions 600 and all public keys to have
                 permissions - 644
           2. Set "PasswordAuthentication no" in /etc/ssh/sshd_config and
              restart the ssh service
        """

        for user in self.users:
            username = user['username']
            home_dir = BASE_HOME_DIR + username
            ssh_dir = os.path.join(home_dir, '.ssh')
            authorized_keys = os.path.join(ssh_dir, 'authorized_keys')
            known_hosts = os.path.join(ssh_dir, 'known_hosts')

            # 1.1-1.2
            run_command(['mkdir', '-p', ssh_dir])
            run_command(['chown', '-R', username + ':' + username, ssh_dir])
            run_command(['chmod', '700', ssh_dir])

            # 1.3-1.5
            run_command(['rm', authorized_keys])
            run_command(['rm', known_hosts])
            run_command(['touch', authorized_keys])
            run_command(['chown', username + ':' + username, authorized_keys])
            run_command(['chmod', '600', authorized_keys])

            # 1.6
            with open(authorized_keys, 'a') as file:
                file.write('\n'.join(user['authorizedKeys']) + '\n')

            # 1.7-1.8
            if user['deleteAllSSHKeys']:
                run_command(['rm', os.path.join(ssh_dir, 'id_*')])
            else:
                run_command(['chmod', '600', os.path.join(ssh_dir, 'id_*')])
                run_command(['chmod', '644',
                             os.path.join(ssh_dir, 'id_*.pub')])

        self._update_sshd_config()
        run_command(['service', 'ssh', 'restart'])

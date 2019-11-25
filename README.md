# Linux Provision Script

This script provisions Linux machines. This script is intended to run on a freshly-installed machine and primarily on Ubuntu-based distros. This script assumes you are running as a non-root user with `sudo` privileges. Run the script with `sudo`.

Copyright 2019 Matthew Sedam. Released under the MIT License.

## Running the Script

To run the script, simply execute the following one-liner. Running the script requires both `git` and `python3`, which are installed by default on Ubuntu-based distros.

```
git clone https://github.com/matthewsedam/linux-provision.git && cd linux-provision && sudo python3 src/main.py
```

## Actions Taken by the Script

The following actions are executed by the script in order.

### User Setup

1. Delete the root password.

### SSH Setup

1. For every user, do the following:
            a. Create `~/.ssh` folder if needed
            b. Set required permissions and ownership on `~/.ssh` folder - `700`
            c. Delete `~/.ssh/authorized_keys`
            d. Delete `~/.ssh/known_hosts`
            e. Create `~/.ssh/authorized_keys` with required permissions and ownership - `600`
            f. For each authorized key, add it to `~/.ssh/authorized_keys`
            g. Remove all `~/.ssh/id_*` if `user["deleteAllSSHKeys"]` is true
            h. If `user["deleteAllSSHKeys"]` is false, set all private keys to have permissions `600` and all public keys to have permissions - `644`
2. Set `PasswordAuthentication no` in `/etc/ssh/sshd_config` and restart the `ssh` service
3. Delete `/root/.ssh`

### Update Setup

1. Updates packages
2. Configures automatic updates.
3. Does full update.

### Port Scanning

1. Run Nmap port scanning on localhost

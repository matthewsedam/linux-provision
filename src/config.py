# config.py
# Copyright 2019 Matthew Sedam
# Released under the MIT License

import json
import logging
import sys


class Config:
    # Holds config internals
    config = None

    # Sets up config
    @staticmethod
    def setup_config():
        if Config.config is not None:
            return Config.config

        Config.setup_config_from_file()
        if Config.config is not None:
            return Config.config

        Config.setup_config_interactive()
        if Config.config is not None:
            return Config.config

        logging.error('Config not properly setup.')
        sys.exit(1)

    # Sets up config from file
    @staticmethod
    def setup_config_from_file():
        if len(sys.argv) < 2:
            return

        logging.info('Reading from config file: ' + sys.argv[1])
        with open(sys.argv[1]) as file:
            try:
                Config.config = json.load(file)
            except:
                logging.error('Error loading config file: ' + sys.argv[1])

    # Sets up config with interaction from the user
    @staticmethod
    def setup_config_interactive():
        # TODO
        pass

    # Returns the config Dict
    @staticmethod
    def get_config():
        return (Config.config if Config.config is not None
                else Config.setup_config())

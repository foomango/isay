"""Configuration"""

__author__ = 'foomango@gmail.com'

import ConfigParser
import os


class Config(object):
    """Configuration
    """

    CONFIG_FILE = os.path.join(os.path.expanduser('~'),
                               '.isay', 'isay.conf')
    SECTION = 'setting'

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(Config.CONFIG_FILE)

    def read(self, name):
        """Read from conf
        Args:
            name: str, key name
            return: str, value
        """
        return self.config.get(Config.SECTION, name).strip()

    def getUsername(self):
        """get user name
        Args:
            return: str, user name
        """
        return self.read('username')

    def getPasswd(self):
        """get password
        Args:
            return: str, password
        """
        return self.read('password')

    def getAutosave(self):
        """get autosave
        Args:
            return: str, autosave
        """
        return self.read('autosave')

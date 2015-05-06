"""Unit test for Config"""

__author__ = 'foomango@gmail.com'


import sys
sys.path.insert(0, '../src')

from unittest import TestCase

from config import Config


class ConfigTestCase(TestCase):
    """Unit test for Config
    """

    def setUp(self):
        Config.CONFIG_FILE = '/tmp/isay/isay.conf'
        self.conf = Config()

    def test_read(self):
        pass

    def test_getUsername(self):
        username = self.conf.getUsername()
        self.assertEquals('test', username)

    def test_getPasswd(self):
        password = self.conf.getPasswd()
        self.assertEquals('test', password)

    def test_getAutosave(self):
        autosave = self.conf.getAutosave()
        self.assertEquals('true', autosave)

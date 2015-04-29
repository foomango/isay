"""Unit test for ShanBay"""

__author__ = 'foomango@gmail.com'


import sys
sys.path.insert(0, '../src')

from unittest import TestCase

from shanbay import ShanBay


class ShanBayTestCase(TestCase):
    """Unit test for ShanBay
    """

    def setUp(self):
        self.shanBay = ShanBay()

    def test_translate(self):
        self.assertTrue('int' in self.shanBay.translate('hi'))

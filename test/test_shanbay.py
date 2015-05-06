"""Unit test for ShanBay"""

__author__ = 'foomango@gmail.com'


import sys
sys.path.insert(0, '../src')

from unittest import TestCase
import os
import cookielib
import urllib2
import urllib

from shanbay import ShanBay
from config import Config


class ShanBayTestCase(TestCase):
    """Unit test for ShanBay
    """

    def setUp(self):
        self.cookiePath = '/tmp/isay/.testcookie.txt'
        cj = cookielib.MozillaCookieJar(self.cookiePath)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.open('http://shanbay.com/accounts/login/')
        cj.save()
        self.cj = cj

        ShanBay.cookiePath = self.cookiePath
        self.shanBay = ShanBay()

        Config.CONFIG_FILE = '/tmp/isay/isay_real.conf'
        self.conf = Config()
        self.shanBay.conf = self.conf

    def login(self):
        username = self.conf.getUsername()
        passwd = self.conf.getPasswd()
        self.shanBay.login(username, passwd)

    def test_getUsername(self):
        username = self.conf.getUsername()
        self.assertEquals(username, self.shanBay.getUsername())

    def test_getPasswd(self):
        passwd = self.conf.getPasswd()
        self.assertEquals(passwd, self.shanBay.getPasswd())

    def test_getAutosave(self):
        autosave = 'true' == self.conf.getAutosave()
        self.assertEquals(autosave, self.shanBay.getAutosave())

    def test_loadCookieJar(self):
        self.shanBay.loadCookieJar()

    def test_translate(self):
        self.login()
        self.assertTrue('int' in self.shanBay.translate('hi'))

    def test_addToLearningList(self):
        jsonData = self.shanBay.addToLearningList(3130)
        self.assertEquals(0, jsonData['status_code'])

    def test_getHeaders(self):
        url = 'http://shanbay.com/accounts/login/'
        headers = self.shanBay.getHeaders(url)
        self.assertGreater(len(headers), 0)

    def test_parseCookies(self):
        headers = []
        headers.append('Set-Cookie: csrftoken=foo; domain=foo.com')
        headers.append('Date: Mon, 04 May 2015 09:58:06 GMT\r\n')
        headers.append('Set-Cookie: user=; domain=foo.com')
        cookies = self.shanBay.parseCookies(headers)
        self.assertEquals('foo', cookies['csrftoken'])
        self.assertEquals('', cookies['user'])

    def test_getJson(self):
        self.login()

        url = 'http://www.shanbay.com/api/v1/bdc/search?%s'
        params = urllib.urlencode({'word': 'hello'})
        jsonData = self.shanBay.getJson(url % params)

        self.assertEquals(0, jsonData['status_code'])

    def test_postJson(self):
        self.login()

        url = 'http://shanbay.com/api/v1/bdc/learning/'
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        data = {"id": 3130, "content_type": "vocabulary"}
        jsonData = self.shanBay.postJson(url, data, headers)
        self.assertEquals(0, jsonData['status_code'])

    def test_login(self):
        self.login()
        self.cj.load()
        sessionid = self.cj._cookies['.shanbay.com']['/']['sessionid'].value
        self.assertNotEquals('', sessionid)

    def test_getCsrftoken(self):
        self.assertNotEquals('', self.shanBay.getCsrftoken())

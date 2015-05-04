"""
Translate word by shanbay.com
"""


__author__ = 'foomango@gmail.com'

import urllib
import urllib2
import cookielib
import json
import re
import os


class ShanBay(object):
    """Translate word by shanbay.com
    """

    cookiePath = os.path.join(os.path.expanduser('~'),
                              'Documents', '.cookie.txt')

    def __init__(self):
        self.url = 'http://www.shanbay.com/api/v1/bdc/search?%s'
        self.loginUrl = 'http://shanbay.com/accounts/login/'
        self.autoSave = True
        self.cj = cookielib.MozillaCookieJar(self.cookiePath)
        self.loadCookieJar()

        if self.autoSave:
            self.opener = urllib2.build_opener(
                urllib2.HTTPCookieProcessor(self.cj))
        else:
            self.opener = urllib2.build_opener()

    def loadCookieJar(self):
        """Load cookies from file, if file does not exist, create it
        """
        try:
            self.cj.load()
        # cookie file not found, create it
        except IOError:
            self.cj.save()

    def translate(self, word):
        """Translate word
        Args:
            word: string, word to be translated
            return: string, meaning
        """

        meaning = 'Unknown'

        params = urllib.urlencode({'word': word})
        url = self.url % params
        data = self.getJson(url, [])

        if data['status_code'] == 0:
            meaning = data['data']['definition']
            if self.autoSave and 'learning_id' not in data['data']:
                print 'TODO'
            else:
                print 'learning_id: ', data['data']['learning_id']
        else:
            meaning = data['msg']

        return meaning

    def request(self, url, params):
        """Send request to shanbay.com
        Args:
            params: dict, parameters
                    url, url to request
            return: file-like object,
        """
        doc = urllib.urlopen(url)
        return doc
        pass

    def getHeaders(self, url):
        """Get http headers
        Args:
            url: string, url to get
            return:
        """
        doc = urllib.urlopen(url)
        return doc.info().headers

    def parseCookies(self, headers):
        """Parse cookies from http headers
        Args:
            headers: list, http headers
            return: dict, cookies
        """
        cookies = {}
        cookieReg = re.compile(r'^Set-Cookie:\s*(\w+)=(\w*);')

        for header in headers:
            m = cookieReg.match(header)
            if m:
                cookies[m.group(1)] = m.group(2)

        return cookies

    def getJson(self, url, headers=[]):
        """Get json from url
        Args:
            url: str, url
            headers: str, headers
            return: json, reponse
        """
        self.opener.addheaders = headers
        response = self.opener.open(url)
        data = response.read()
        jsonData = json.loads(data)

        if self.autoSave:
            self.cj.save()
        return jsonData

    def postJson(self, url, data, headers=[]):
        """Post json to url
        Args:
            url: str, url
            data: list, data
            headers: list, headers
        """
        extraHeaders = {'content-type': 'application/json'}
        cookies = 'sessionid=' +\
            self.cj._cookies['.shanbay.com']['/']['sessionid'].value
        cookiesHeader = {'Cookie:': cookies}
        headers.update(extraHeaders)
        headers.update(cookiesHeader)
        data = json.dumps(data)

        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        rawData = resp.read()
        jsonData = json.loads(rawData)

        return jsonData

    def login(self, name, passwd):
        """Login shanbay.com
        Args:
            name: str, user name
            passwd: str, password
        """

        class NoRedirection(urllib2.HTTPErrorProcessor):
            def http_response(self, request, response):
                return response

        # empty cookie
        self.cj.clear()

        # get csrf
        self.opener.open(self.loginUrl)

        # login
        loginData = urllib.urlencode({
            'csrfmiddlewaretoken': self.getCsrftoken(),
            'username': name,
            'password': passwd
        })
        opener = urllib2.build_opener(NoRedirection,
                                      urllib2.HTTPCookieProcessor(self.cj))
        response = opener.open(self.loginUrl, loginData)
        if response.getcode() != 302:
            print '[Warning] Login failed'
        self.cj.save()

    def getCsrftoken(self):
        """Get csrftoken
        Args:
            return: string, csrftoken
        """

        csrftoken = ''

        try:
            csrftoken = self.cj._cookies['.shanbay.com']['/']['csrftoken'].value
        except Exception:
            csrftoken = ''

        return csrftoken

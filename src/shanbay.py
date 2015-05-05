"""
Translate word by shanbay.com
"""


__author__ = 'foomango@gmail.com'

import urllib
import json


class ShanBay(object):
    """Translate word by shanbay.com
    """

    def __init__(self):
        self.url = 'http://www.shanbay.com/api/v1/bdc/search?%s'

    def translate(self, word):
        """Translate word
        Args:
            word: string, word to be translated
            return: string, meaning
        """

        meaning = 'Unknown'

        params = urllib.urlencode({'word': word})
        doc = urllib.urlopen(self.url % params)
        resp = doc.read()
        data = json.loads(resp)

        if data['status_code'] == 0:
            meaning = data['data']['definition']
            meaning = meaning.replace('\n', '\n ')
        else:
            meaning = data['msg']

        return meaning

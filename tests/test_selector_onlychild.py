#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.onlychild import OnlyChild

class TestOnlyChildSelector(unittest.TestCase):
    def setUp(self):
        self.oc = OnlyChild('h1')
        self.node = xml.dom.minidom.parseString('<div><h1><h1>1</h1><h2>2</h2></h1></div>').firstChild
    def test_match(self):
        self.assertTrue(self.oc.match(self.node.firstChild))
        self.assertFalse(self.oc.match(self.node.firstChild.firstChild))

if __name__ == '__main__':
    unittest.main()

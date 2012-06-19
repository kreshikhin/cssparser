#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.child import Child

class TestChildSeltctor(unittest.TestCase):
    def setUp(self):
        self.child = Child('div','h1')
        self.dom = xml.dom.minidom.parseString('<div><h1><h2><p>hello</p></h2></h1></div>')

    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.child.match(self.node))
        self.node = self.node.firstChild
        self.assertTrue(self.child.match(self.node))
        self.node = self.node.firstChild
        self.assertFalse(self.child.match(self.node))

if __name__ == '__main__':
    unittest.main()

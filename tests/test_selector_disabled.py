#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.disabled import Disabled

class TestEnabledSelector(unittest.TestCase):
    def setUp(self):
        self.r = Disabled('h1')
        self.node = xml.dom.minidom.parseString('<div><b><h1 disabled="">test</h1></b></div>').firstChild
        
    def test_match(self):
        self.assertFalse(self.r.match(self.node))
        self.assertFalse(self.r.match(self.node.firstChild))
        self.assertTrue(self.r.match(self.node.firstChild.firstChild))

class TestEnabledSelector2(unittest.TestCase):
    def setUp(self):
        self.r = Disabled('h1','e')
        self.node = xml.dom.minidom.parseString('<div><b><h1>test</h1></b></div>').firstChild
        
    def test_match(self):
        self.assertFalse(self.r.match(self.node))
        self.assertFalse(self.r.match(self.node.firstChild))
        self.assertTrue(self.r.match(self.node.firstChild.firstChild))

if __name__ == '__main__':
    unittest.main()

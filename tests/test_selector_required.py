#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.required import Required

class TestRequiredSelector(unittest.TestCase):
    def setUp(self):
        self.r = Required('h1')
        self.node = xml.dom.minidom.parseString('<div><b><h1 required="">test</h1></b></div>').firstChild
        
    def test_match(self):
        self.assertFalse(self.r.match(self.node))
        self.assertFalse(self.r.match(self.node.firstChild))
        self.assertTrue(self.r.match(self.node.firstChild.firstChild))

class TestRequiredSelector2(unittest.TestCase):
    def setUp(self):
        self.r = Required('h1','o')
        self.node = xml.dom.minidom.parseString('<div><b><h1 required="">test</h1></b></div>').firstChild
        
    def test_match(self):
        self.assertFalse(self.r.match(self.node))
        self.assertFalse(self.r.match(self.node.firstChild))
        self.assertFalse(self.r.match(self.node.firstChild.firstChild))

if __name__ == '__main__':
    unittest.main()

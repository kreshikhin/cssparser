#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.readonly import ReadOnly

class TestReadOnlySelector(unittest.TestCase):
    def setUp(self):
        self.ro = ReadOnly('h1')
        self.node = xml.dom.minidom.parseString('<div><b><h1 readonly>test</h1></b></div>').firstChild
        
    def test_match(self):
        self.assertFalse(self.ro.match(self.node))
        self.assertFalse(self.ro.match(self.node.firstChild))
        self.assertTrue(self.ro.match(self.node.firstChild.firstChild))

class TestReadOnlySelector2(unittest.TestCase):
    def setUp(self):
        self.ro = ReadOnly('h1', 'w')
        self.node = xml.dom.minidom.parseString('<div><b><h1 readonly="" >test</h1></b></div>').firstChild
        
    def test_match(self):
        self.assertFalse(self.ro.match(self.node))
        self.assertFalse(self.ro.match(self.node.firstChild))
        self.assertFalse(self.ro.match(self.node.firstChild.firstChild))

if __name__ == '__main__':
    unittest.main()


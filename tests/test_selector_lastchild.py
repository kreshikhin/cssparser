#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.lastchild import LastChild

class TestLastChild(unittest.TestCase):
    def setUp(self):
        self.lc1=LastChild('h2')
        self.lc2=LastChild('h1')
        self.node = xml.dom.minidom.parseString('<div><h1>ne</h1><h2></h2></div>').firstChild
        
    def test_match(self):
        self.assertTrue(self.lc1.match(self.node.lastChild))
        self.assertFalse(self.lc2.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.nthlastchild import NthLastChild

class TestNthLastChild(unittest.TestCase):
    def setUp(self):
        self.lc1=NthLastChild('h2',1)
        self.lc2=NthLastChild('h2',2)
        self.node = xml.dom.minidom.parseString('<div><h1>ne</h1><h2></h2></div>').firstChild
        
    def test_match(self):
        self.assertTrue(self.lc1.match(self.node.firstChild.nextSibling))
        self.assertFalse(self.lc2.match(self.node.firstChild.nextSibling))

if __name__ == '__main__':
    unittest.main()

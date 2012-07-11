#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.nthchild import NthChild

class TestNthChildSelector(unittest.TestCase):
    def setUp(self):
        self.lc1=NthChild('h2',2)
        self.lc2=NthChild('h2',1)
        self.node = xml.dom.minidom.parseString('<div><h2>ne</h2><h2></h2></div>').firstChild

    def test_match(self):
        self.assertTrue(self.lc1.match(self.node.firstChild.nextSibling))
        self.assertTrue(self.lc2.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()

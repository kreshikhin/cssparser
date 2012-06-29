#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.nthoftype import NthOfType

class TestFirstOfTypeSelector(unittest.TestCase):
    def setUp(self):
        self.not1 = NthOfType('h1',1)
        self.not2 = NthOfType('h1',2)
        self.not3 = NthOfType('b',1)
        self.node = xml.dom.minidom.parseString('<div><h1>1</h1><b>2</b><h1><h1>3.1</h1></h1></div>').firstChild

    def test_match(self):
        self.assertTrue(self.not1.match(self.node.firstChild))
        self.assertTrue(self.not2.match(self.node.lastChild))
        self.assertFalse(self.not2.match(self.node.firstChild))
        self.assertFalse(self.not1.match(self.node.lastChild))
        self.assertTrue(self.not3.match(self.node.firstChild.nextSibling))

if __name__ == '__main__' :
    unittest.main()

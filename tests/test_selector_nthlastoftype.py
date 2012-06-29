#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.nthlastoftype import NthLastOfType

class TestNthLastOfTypeSelector(unittest.TestCase):
    def setUp(self):
        self.nlot1 = NthLastOfType('h1',2)
        self.nlot2 = NthLastOfType('b',1)
        self.node = xml.dom.minidom.parseString('<div><h1></h1><b></b><h1></h1></div>').firstChild
   
    def test_match(self):
        self.assertTrue(self.nlot1.match(self.node.firstChild))
        self.assertFalse(self.nlot1.match(self.node.lastChild))
        self.assertTrue(self.nlot2.match(self.node.firstChild.nextSibling))
        self.assertFalse(self.nlot2.match(self.node.lastChild))
        self.assertFalse(self.nlot2.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()

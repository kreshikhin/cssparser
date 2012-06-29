#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.firstoftype import FirstOfType

class TestFirstOfTypeSelector(unittest.TestCase):
    def setUp(self):
        self.fot1 = FirstOfType('b')
        self.fot2 = FirstOfType('h1')
        self.node = xml.dom.minidom.parseString('<div><h1></h1><b></b><h1></h1></div>').firstChild

    def test_match(self):
        self.assertTrue(self.fot1.match(self.node.firstChild.nextSibling))
        self.assertTrue(self.fot2.match(self.node.firstChild))
        self.assertFalse(self.fot2.match(self.node.lastChild))
        self.assertFalse(self.fot1.match(self.node.firstChild))

if __name__ == '__main__' :
    unittest.main()

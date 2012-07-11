#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.lastoftype import LastOfType

class TestLastOfTypeSelector(unittest.TestCase):
    def setUp(self):
        self.lot1 = LastOfType('h1')
        self.lot2 = LastOfType('b')
        self.node = xml.dom.minidom.parseString('<div><h1></h1><b></b><h1></h1></div>').firstChild

    def test_match(self):
        self.assertFalse(self.lot1.match(self.node.firstChild))
        self.assertTrue(self.lot1.match(self.node.lastChild))
        self.assertFalse(self.lot2.match(self.node.firstChild))
        self.assertTrue(self.lot2.match(self.node.firstChild.nextSibling))
        self.assertFalse(self.lot1.match(self.node.firstChild.nextSibling))
if __name__ == '__main__':
    unittest.main()


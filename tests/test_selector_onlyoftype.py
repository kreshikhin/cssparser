#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.onlyoftype import OnlyOfType

class TestOnlyOfTypeSelector(unittest.TestCase):
    def setUp(self):
        self.ot1 = OnlyOfType('h1')
        self.ot2 = OnlyOfType('b')
        self.node = xml.dom.minidom.parseString('<div><h1></h1><b></b><h1></h1></div>').firstChild

    def test_match(self):
        self.assertFalse(self.ot1.match(self.node.firstChild))
        self.assertFalse(self.ot1.match(self.node.lastChild))
        self.assertFalse(self.ot2.match(self.node.firstChild))
        self.assertTrue(self.ot2.match(self.node.firstChild.nextSibling))

if __name__ == '__main__':
    unittest.main()

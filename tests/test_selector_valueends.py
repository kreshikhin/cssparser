#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.valueends import ValueEnds

class TestSelectorValueEnds(unittest.TestCase):
    def setUp(self):
        self.ve = ValueEnds('h1','att','lue')
        self.node = xml.dom.minidom.parseString('<div><h1 att="value">bar</h1></div>').firstChild
   
    def test_match(self):
        self.assertFalse(self.ve.match(self.node))
        self.assertTrue(self.ve.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()

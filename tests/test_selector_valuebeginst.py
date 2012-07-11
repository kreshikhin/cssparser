#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.valuebeginst import ValueBeginst

class TestValueBeginstSelector(unittest.TestCase):
    def setUp(self):
        self.vb = ValueBeginst('h1','att','val')
        self.node = xml.dom.minidom.parseString('<div><h1 att="value">bar</h1></div>').firstChild

    def test_match(self):
        self.assertFalse(self.vb.match(self.node))
        self.assertTrue(self.vb.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.parent import Parent

class TestParentSelector(unittest.TestCase):
    def setUp(self):
        self.dom = xml.dom.minidom.parseString('<div><b><h1>test</h1></b></div>')
        self.parent = Parent('div','h1')

    def test_match(self):
        node = self.dom.firstChild
        self.assertTrue(self.parent.match(node))
        node = node.firstChild
        self.assertFalse(self.parent.match(node))
        self.assertFalse(self.parent.match(node.firstChild))

if __name__ == '__main__':
    unittest.main()
        

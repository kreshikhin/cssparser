#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.empty import Empty

class TestEmptySelector(unittest.TestCase):
    def setUp(self):
        self.em1 = Empty('h1')
        self.em2 = Empty('h2')
        self.node = xml.dom.minidom.parseString('<div><h1>ne</h1><h2></h2></div>').firstChild

    def test_match(self):
        self.assertFalse(self.em1.match(self.node.firstChild))
        self.assertTrue(self.em2.match(self.node.firstChild.nextSibling))

if __name__ == '__main__':
    unittest.main()


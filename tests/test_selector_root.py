#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.root import Root

class TestRootSelector(unittest.TestCase):
    def setUp(self):
        self.r = Root('div')
        self.node = xml.dom.minidom.parseString('<div><b><h1>t</h1></b></div>').firstChild
   
    def test_match(self):
        self.assertTrue(self.r.match(self.node))
        self.assertFalse(self.r.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()
    

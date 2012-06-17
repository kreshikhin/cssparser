#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.universal import Universal

class TestUniversalSelector(unittest.TestCase):
    def setUp(self):
        self.selector = Universal()
        self.dom = xml.dom.minidom.parseString('<div><p>hello</p></div>');
    
    def test_match(self):
        node = self.dom.firstChild
        result = self.selector.match(node)
        self.assertTrue(result)
        
if __name__ == '__main__':
    unittest.main()

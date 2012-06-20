#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.type import Type

class TestCss2Py(unittest.TestCase):
    def setUp(self):
        self.selector = Type('p')
        self.dom = xml.dom.minidom.parseString('<div><p>hello</p></div>');
    
    def test_match(self):
        divNode = self.dom.firstChild
        self.assertFalse(self.selector.match(divNode))
        pNode = divNode.firstChild
        self.assertTrue(self.selector.match(pNode))
        
if __name__ == '__main__':
    unittest.main()

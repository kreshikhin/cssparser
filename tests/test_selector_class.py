#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.class_ import Class

class TestClassSelector(unittest.TestCase):
    def setUp(self):
        self.class_ = Class('ny')
        self.dom = xml.dom.minidom.parseString('<div><h1>b</h1><h2 class="nya" a="5">p</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.class_.match(self.node))
        self.node = self.node.firstChild.nextSibling
        self.assertTrue(self.class_.match(self.node))
        
if __name__ == '__main__':
   unittest.main()

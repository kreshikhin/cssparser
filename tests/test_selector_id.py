#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.id import Id

class TestIdSelector1(unittest.TestCase):
    def setUp(self):
        self.id = Id('h2','174')
        self.dom = xml.dom.minidom.parseString('<div><h1>b</h1><h2 id="174" a="5">p</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.id.match(self.node))
        self.node = self.node.firstChild.nextSibling
        self.assertTrue(self.id.match(self.node))

class TestIdSelector2(unittest.TestCase):
    def setUp(self):
        self.id = Id('h1','174')
        self.dom = xml.dom.minidom.parseString('<div><h1>b</h1><h2 id="174" a="5">p</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.id.match(self.node))
        self.node = self.node.firstChild.nextSibling
        self.assertFalse(self.id.match(self.node))
        
if __name__ == '__main__':
   unittest.main()

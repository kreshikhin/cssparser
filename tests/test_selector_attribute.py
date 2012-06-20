#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.attribute import Attribute

class TestAttributeSelector(unittest.TestCase):
    def setUp(self):
        self.attribute = Attribute('attr')
        self.dom = xml.dom.minidom.parseString('<div><h1>bla</h1><h2 attr="nya" a="5">bl</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.attribute.match(self.node))
        self.node = self.node.firstChild
        self.assertTrue(self.attribute.match(self.node.nextSibling))

class TestAttributeSelector2(unittest.TestCase):
    def setUp(self):
        self.attribute = Attribute('attr', 'nya')
        self.dom = xml.dom.minidom.parseString('<div><h1>bla</h1><h2 attr="nya" a="5">bl</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.attribute.match(self.node))
        self.node = self.node.firstChild
        self.assertTrue(self.attribute.match(self.node.nextSibling))

class TestAttributeSelector3(unittest.TestCase):
    def setUp(self):
        self.attribute = Attribute('attr', 'nya','ny')
        self.dom = xml.dom.minidom.parseString('<div><h1>bla</h1><h2 attr="nya" a="5">bl</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild
        self.assertFalse(self.attribute.match(self.node))
        self.node = self.node.firstChild
        self.assertTrue(self.attribute.match(self.node.nextSibling))

if __name__ == '__main__':
   unittest.main()

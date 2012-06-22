#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.pseudoclass import Pseudoclass

class TestSelectorPseudoclass(unittest.TestCase):
    def setUp(self):
        self.pclass = Pseudoclass('h1','div')
        self.dom = xml.dom.minidom.parseString('<div><h1>b</h1><h2 id="174" a="5">p</h2></div>')
    def test_match(self):
        self.node = self.dom.firstChild.firstChild
        self.assertTrue(self.pclass.match(self.node))
        self.assertFalse(self.pclass.match(self.node.nextSibling))

if __name__ == '__main__':
   unittest.main()

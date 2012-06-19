#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.descendant import Descendant

class TestDescendantSelectorDiv(unittest.TestCase):
      def setUp(self):
          self.selectorp=Descendant('div','p')
          self.selectordiv=Descendant('p','div')
          self.dom = xml.dom.minidom.parseString('<div><h1><h2><p>hello</p></h2></h1></div>')
          
      def test_match(self):
          self.NodeDiv = self.dom.firstChild
          self.assertFalse(self.selectordiv.match(self.NodeDiv))
          self.Nodep = self.NodeDiv.firstChild
          for i in range(2):
             self.Nodep = self.Nodep.firstChild             
          self.assertTrue(self.selectorp.match(self.Nodep))

if __name__ == '__main__':
    unittest.main()

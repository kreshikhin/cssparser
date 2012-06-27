#!/usr/bin/env python3.2
# coding=utf-8

import unittest

import sys
sys.path.append('../src/')

import xml.dom.minidom
from selector.caseins import CaseIns

class TestCaseInsSelector(unittest.TestCase):
    def setUp(self):
        self.obj = CaseIns('b','val','TeSt')
        self.node = xml.dom.minidom.parseString('<div><b val="test">bar</b></div>').firstChild
    def test_match(self):
        self.assertFalse(self.obj.match(self.node))
        self.assertTrue(self.obj.match(self.node.firstChild))

if __name__ == '__main__':
    unittest.main()

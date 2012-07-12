#!/usr/bin/env python3.2
# coding=utf-8

import unittest
import css2py.cssparser as cssparser

class SpecializedParser(cssparser.CSSParser):
    def handle_charset(self, charset):
        print("parsed charset:", charset)
    
        
class TestCSSParser(unittest.TestCase):
    def setUp(self):
        self.parser = SpecializedParser()
        self.css_data = """
        @charset "utf-8";
        body > div{
            color: red;
        }
        """
    def test_feed(self):
        self.parser.feed(self.css_data)

if __name__ == '__main__':
   unittest.main()

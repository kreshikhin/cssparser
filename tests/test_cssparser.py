#!/usr/bin/env python3.2
# coding=utf-8

import unittest
import css2py.cssparser as cssparser

class SpecialParser(cssparser.CSSParser):
    def handle_selector(self, selector):
        pass
    
    def handle_ruleset(self, ruleset):
        pass
    
    def handle_charset(self, charset):
        pass
    
    def handle_declaration(self, declaration):
        pass
        
class TestCSSParser(unittest.TestCase):
    def setUp(self):
        self.parser = cssparser.CSSParser()
        self.css_data =
        """
        body > div{
            color: red;
        }
        """
    def test_feed(self):
        self.parser.feed(self.css_data)

if __name__ == '__main__':
   unittest.main()

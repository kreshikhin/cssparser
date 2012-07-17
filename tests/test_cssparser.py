#!/usr/bin/env python3.2
# coding=utf-8

import unittest
import cssparser

css_data = """@charset "utf-8";

.sportid-logo
{
    background-color: white;
    color: #265581;
    position: relative;
    top: 2px;
    margin: 3px;
    margin-top: 10px;
    padding: 2px;
    border: 1px solid #265581; 
    border-radius: 3px;
    font-family: 'Arial', bold;
    font-size: 12pt;
}


*div
{
    color:red;
}

:focus{
    font-size: 12pt;
}

.juggler:link, .juggler:visited, .juggler:active, .juggler:focus
{
    text-decoration: none;
    font-family: 'Lobster', cursive;
    font-size: 18pt;
    color: #246;
}


.block
{
    text-align: justify;
    float: left;
    margin: 10px;
    width: 300px;
    height: 200px;
    color: #123;;
    font-family: 'EB Garamond';
    font-size: 13pt;
    line-height: 1.1;
}

body > footer
{
    margin: -10px;
    height: 200px;
}

body + footer
{
    height: 100%;
    color: #ABD;
}

body footer ul li
{
    text-decoration: none;
    color: #CCF;
    padding-left: 0px;
    font-family: 'Poiret One';
    font-size: 16pt;
    list-style-type: none;
}

body footer a:link, a:active, a:focus, a:visited
{
    color: #246;
    text-decoration: none;
}

body footer a:hover
{
    color: #246;
    text-decoration: underline;
}


#bbbody footer .industry
{
}

input[type="text"]
{
    margin: 0px;
    background-color: #EEE;
}

input[class~="special"]
{
    margin: 0px;
    background-color: #EEE;
}
"""

class SpecializedParser(cssparser.CSSParser):
    def handle_charset(self, charset):
        print("Encountered a charset:", charset)
    
    def handle_combinator(self, combinator):
        print("Encountered a combinator:", combinator)
    
    def handle_selector(self, selector_type, selector_name = '', selector_attribute = '', attribute_value = ''):
        print("Encountered a selector:", selector_type, selector_name, selector_attribute, attribute_value)
    
    def handle_separator(self):
        print("Encountered a separator")
        
    def handle_declaration(self, property_name, value):
        print("Encountered a declaration:", property_name, value)

class TestCSSParser(unittest.TestCase):
    def setUp(self):
        self.parser = cssparser.CSSParser
        
    def test_feed(self):
        self.parser.feed(css_data)

class TestCSSParser(unittest.TestCase):
    def setUp(self):
        self.parser = SpecializedParser()

    def test_feed(self):
        self.parser.feed(css_data)

if __name__ == '__main__':
   unittest.main()

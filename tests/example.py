#!/usr/bin/env python3.2
# coding=utf-8

import cssparser

class MyCSSParser(cssparser.CSSParser):
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
        
parser = MyCSSParser()
parser.feed(
"""@charset "utf-8";

div.logo
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

""")

parser.close()

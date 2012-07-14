#!/usr/bin/env python3.2
# coding=utf-8

import unittest
import css2py.cssparser as cssparser

class SpecializedParser(cssparser.CSSParser):
    def handle_charset(self, charset):
        print("### parsed charset:", charset)
    
        
class TestCSSParser(unittest.TestCase):
    def setUp(self):
        self.parser = SpecializedParser()
        self.css_data = """@charset "urf-8";
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

.sportid-logo-id
{
    background-color: #D32027;
    color: white;
    border-radius: 3px;
    margin-left: 2px;
    padding-left: 2px;
    padding-right: 2px;
}

.eng, .portfolio
{
    display: none;
}

body
{
    margin: 0px;
    background-color: #EEE;
}

body a
{
    text-decoration: none;
    border: 0px;
}
body a:focus
{
    outline: 0px;
}

body header
{
    background-color: #246;
    margin-top: -2px;
}

body header .industry
{
    background-color: #246;
}

body header ul
{
    margin-top: 5px;
}

body header ul li
{
    color: #FFF;
    font-size: 18pt;
    display: inline;
    border-left: 0px solid;
    padding-left: 20px;
    font-family: 'Poiret One';
    padding: 15px;
    padding-top: 10px;
    padding-bottom: 0px;
    list-style-type: none;
}

.selected
{
    background-color: #DDD;
    color: #123;
    border: #DDD 1px solid;
    border-radius: 15px;
    padding: 14px;
    padding-top: 10px;
    padding-bottom: 0px;
}

body .logo
{
    width: 100px;
    height: 40px;
    padding: 15px;
    padding-left: 15px;
    color: #DDD;
    outline: 0px;
    font-family: 'Russo One', normal;
}

body .square
{
    width: 30px;
    height: 30px;
    border: 5px solid;
    border-right: 10px solid;
    border-color: #DDD;
    border-radius: 3px;
}

body .open
{
    margin-top: -13px;
    margin-left: 42px;
    font-size: 16pt;
}

body .industry
{
    width: 100px;
    margin-top: 2px;
    margin-left: 16px;
    font-size: 16pt;
}

body section
{
    margin: 0px;
    background-color: #DDD;
}

body section h1
{
    color: #124;
    font-family: 'Forum';
    font-weight: normal;
    font-size: 18pt;
    margin-bottom: 2px;
}

body section .text
{
    text-align: justify;
    padding-top: 50px;
    margin: auto;
    width: 960px;
    height: 150px;
    font-family: 'EB Garamond';
    font-size: 13pt;
    color: #123;
    line-height: 1.1;
}

.juggler:link, .juggler:visited, .juggler:active, .juggler:focus
{
    text-decoration: none;
    font-family: 'Lobster', cursive;
    font-size: 18pt;
    color: #246;
}

.juggler:hover
{
    color: #246;
    text-decoration: underline;
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

.wideblock
{
    text-align: justify;
    float: left;
    margin: 10px;
    width: 620px;
    height: 200px;
    color: #123;;
    font-family: 'EB Garamond';
    font-size: 13pt;
    line-height: 1.1;
}

body footer
{
    margin: -10px;
    height: 200px;
}

body footer
{
    height: 100%;
    color: #ABD;
}

body footer ul
{
    margin-top: 5px;
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

body footer ul li a
{
    text-decoration: none;
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

body footer .logo
{
    color: #CCC;
}

body footer .square
{
    border-color: #CCC;
}

body footer .industry
{
    background-color: #EEE;
}

        """

    def test_feed(self):
        self.parser.feed(self.css_data)

if __name__ == '__main__':
   unittest.main()

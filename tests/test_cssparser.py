#!/usr/bin/env python3

import unittest

import cssparser


class Collector(cssparser.CSSParser):
    def __init__(self, strict=True):
        super().__init__(strict=strict)
        self.events = []

    def handle_charset(self, charset):
        self.events.append(("charset", charset))

    def handle_selector(self, selector_type, name="", predicate="", value=""):
        self.events.append(("selector", selector_type, name, predicate, value))

    def handle_combinator(self, combinator):
        self.events.append(("combinator", combinator))

    def handle_separator(self):
        self.events.append(("separator",))

    def handle_declaration(self, property_name, value):
        self.events.append(("declaration", property_name, value))


def parse(css, strict=True):
    parser = Collector(strict=strict)
    parser.feed(css)
    parser.close()
    return parser.events


class CSSParserTests(unittest.TestCase):
    def test_readme_example(self):
        events = parse(
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
"""
        )
        self.assertEqual(
            events,
            [
                ("charset", '"utf-8"'),
                ("selector", "type", "div", "", ""),
                ("selector", "class", "logo", "", ""),
                ("declaration", "background-color", "white"),
                ("declaration", "color", "#265581"),
                ("declaration", "position", "relative"),
                ("declaration", "top", "2px"),
                ("declaration", "margin", "3px"),
                ("declaration", "margin-top", "10px"),
                ("declaration", "padding", "2px"),
                ("declaration", "border", "1px solid #265581"),
                ("declaration", "border-radius", "3px"),
                ("declaration", "font-family", "'Arial', bold"),
                ("declaration", "font-size", "12pt"),
            ],
        )

    def test_default_handlers_accept_valid_css(self):
        parser = cssparser.CSSParser()
        parser.feed("div { color: red }")
        parser.close()

    def test_selectors_combinators_and_attributes(self):
        events = parse(
            """
            h1, h2.x { color: red }
            body > div + p span { color: blue }
            div.logo#brand:hover { color: green }
            * > a[href] { color: black }
            input[type="text"] { margin: 0px }
            input[class~=special] { margin: 1px }
            a[lang|="en"] { color: #abc }
            :lang(en) { quotes: none }
            """
        )
        self.assertEqual(
            events,
            [
                ("selector", "type", "h1", "", ""),
                ("separator",),
                ("selector", "type", "h2", "", ""),
                ("selector", "class", "x", "", ""),
                ("declaration", "color", "red"),
                ("selector", "type", "body", "", ""),
                ("combinator", ">"),
                ("selector", "type", "div", "", ""),
                ("combinator", "+"),
                ("selector", "type", "p", "", ""),
                ("combinator", " "),
                ("selector", "type", "span", "", ""),
                ("declaration", "color", "blue"),
                ("selector", "type", "div", "", ""),
                ("selector", "class", "logo", "", ""),
                ("selector", "id", "brand", "", ""),
                ("selector", "pseudo", "hover", "", ""),
                ("declaration", "color", "green"),
                ("selector", "type", "*", "", ""),
                ("combinator", ">"),
                ("selector", "type", "a", "", ""),
                ("selector", "attribute", "href", "", ""),
                ("declaration", "color", "black"),
                ("selector", "type", "input", "", ""),
                ("selector", "attribute", "type", "=", '"text"'),
                ("declaration", "margin", "0px"),
                ("selector", "type", "input", "", ""),
                ("selector", "attribute", "class", "~=", "special"),
                ("declaration", "margin", "1px"),
                ("selector", "type", "a", "", ""),
                ("selector", "attribute", "lang", "|=", '"en"'),
                ("declaration", "color", "#abc"),
                ("selector", "pseudo", "lang", "", "en"),
                ("declaration", "quotes", "none"),
            ],
        )


if __name__ == "__main__":
    unittest.main()

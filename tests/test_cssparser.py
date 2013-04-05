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

    def test_values_important_and_functions(self):
        events = parse(
            """
            p {
                margin: -10px;
                height: 100%;
                line-height: 1.1;
                font: italic small-caps 12pt/14pt Arial, sans-serif;
                color: red !important;
                background: rgb(1, 2, 3);
                width: 2em;
            }
            """
        )
        declarations = [event for event in events if event[0] == "declaration"]
        self.assertEqual(
            declarations,
            [
                ("declaration", "margin", "-10px"),
                ("declaration", "height", "100%"),
                ("declaration", "line-height", "1.1"),
                ("declaration", "font", "italic small-caps 12pt/14pt Arial, sans-serif"),
                ("declaration", "color", "red !important"),
                ("declaration", "background", "rgb(1, 2, 3)"),
                ("declaration", "width", "2em"),
            ],
        )

    def test_at_rules(self):
        events = parse(
            """
            @import "a.css";
            @import url("b.css") print, screen;
            @media screen, print {
                div { color: red }
            }
            @page :first { margin: 1cm }
            @page { margin: 2cm }
            """
        )
        self.assertEqual(
            events,
            [
                ("selector", "type", "div", "", ""),
                ("declaration", "color", "red"),
                ("selector", "pseudo", "first", "", ""),
                ("declaration", "margin", "1cm"),
                ("declaration", "margin", "2cm"),
            ],
        )

    def test_comments_and_cdata_markers(self):
        events = parse(
            """
            <!--
            div { color: /* no */ blue }
            -->
            """
        )
        self.assertEqual(
            events,
            [
                ("selector", "type", "div", "", ""),
                ("declaration", "color", "blue"),
            ],
        )

    def test_empty_declarations_and_omitted_semicolon(self):
        events = parse("div { color: #123;; margin: 0 }")
        self.assertEqual(
            events,
            [
                ("selector", "type", "div", "", ""),
                ("declaration", "color", "#123"),
                ("declaration", "margin", "0"),
            ],
        )

    def test_incremental_feed_and_reset(self):
        parser = Collector()
        parser.feed("div { color: ")
        self.assertEqual(parser.events, [])
        parser.feed("red }")
        parser.close()
        self.assertEqual(
            parser.events,
            [
                ("selector", "type", "div", "", ""),
                ("declaration", "color", "red"),
            ],
        )

        parser.reset()
        parser.events.clear()
        parser.feed("span { color: ")
        parser.reset()
        parser.feed("em { color: blue }")
        parser.close()
        self.assertEqual(
            parser.events,
            [
                ("selector", "type", "em", "", ""),
                ("declaration", "color", "blue"),
            ],
        )

    def test_strict_error_exposes_position(self):
        parser = Collector()
        with self.assertRaises(cssparser.CSSParseError) as caught:
            parser.feed("*div { color: red }\n")
            parser.close()
        error = caught.exception
        self.assertIsInstance(error.msg, str)
        self.assertTrue(error.msg)
        self.assertEqual(error.lineno, 1)
        self.assertGreaterEqual(error.offset, 0)
        self.assertIn(error.msg, str(error))
        self.assertEqual(parser.events, [])

    def test_strict_error_on_later_line(self):
        parser = Collector()
        parser.feed("div { color: red }\n")
        with self.assertRaises(cssparser.CSSParseError) as caught:
            parser.feed("span { color: ; }\n")
            parser.close()
        self.assertEqual(caught.exception.lineno, 2)
        self.assertEqual(
            parser.events,
            [
                ("selector", "type", "div", "", ""),
                ("declaration", "color", "red"),
            ],
        )

    def test_strict_invalid_hex_color(self):
        parser = Collector()
        with self.assertRaises(cssparser.CSSParseError) as caught:
            parser.feed("div { color: #abcd }")
            parser.close()
        self.assertEqual(caught.exception.msg, "invalid hex color")
        self.assertEqual(parser.events, [])

    def test_nonstrict_skips_bad_selector_and_declaration(self):
        events = parse(
            """
            *div { color: red }
            div, *div { color: green }
            p { color: #abcd; height: 10px; width: 12turn; margin: 1px }
            """,
            strict=False,
        )
        self.assertEqual(
            events,
            [
                ("selector", "type", "p", "", ""),
                ("declaration", "height", "10px"),
                ("declaration", "margin", "1px"),
            ],
        )

    def test_original_stylesheet_sample(self):
        events = parse(
            """@charset "utf-8";

.sportid-logo
{
    background-color: white;
    color: #265581;
    font-size: 12pt;
}

:focus { font-size: 12pt; }

.juggler:link, .juggler:visited { color: #246; }

body > footer { margin: -10px; }
body + footer { height: 100%; }
body footer ul li { color: #CCF; }
#bbbody footer .industry { }
input[type="text"] { background-color: #EEE; }
input[class~="special"] { background-color: #EEE; }
"""
        )
        self.assertEqual(events[0], ("charset", '"utf-8"'))
        self.assertIn(("selector", "class", "sportid-logo", "", ""), events)
        self.assertIn(("selector", "pseudo", "focus", "", ""), events)
        self.assertIn(("separator",), events)
        self.assertIn(("combinator", ">"), events)
        self.assertIn(("combinator", "+"), events)
        self.assertIn(("combinator", " "), events)
        self.assertIn(("selector", "id", "bbbody", "", ""), events)
        self.assertIn(("selector", "attribute", "type", "=", '"text"'), events)
        self.assertIn(("selector", "attribute", "class", "~=", '"special"'), events)
        self.assertIn(("declaration", "margin", "-10px"), events)
        self.assertIn(("declaration", "height", "100%"), events)


if __name__ == "__main__":
    unittest.main()

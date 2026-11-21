# cssparser

[![CI](https://github.com/kreshikhin/cssparser/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/kreshikhin/cssparser/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![CSS 2.1](https://img.shields.io/badge/CSS-2.1-264de4)](https://www.w3.org/TR/CSS21/grammar.html)

Python extension that parses [CSS 2.1](https://www.w3.org/TR/CSS21/grammar.html) and reports it as a sequence of events. Subclass `CSSParser`, feed it a stylesheet, and override the handlers for charset rules, selectors, combinators, and declarations.

The grammar follows the W3C CSS 2.1 lex/yacc specification. The parser is a C extension built with flex and bison.

## Requirements

- Python 3.10 or newer
- flex
- bison 2.3 or newer
- A C compiler (`clang` on macOS, `gcc` on Linux)

`setuptools` is used when it is installed. Without it, `python3 setup.py build_ext --inplace` compiles the extension directly. That fallback is macOS-only.

## Build

```bash
python3 setup.py build_ext --inplace
```

The extension is written next to `setup.py` as `cssparser*.so`. Import it from that directory, or set `PYTHONPATH` to the repository root.

```bash
python3 -m unittest tests.test_cssparser
```

`tests/example.py` is a small demo of the same stylesheet used below. Run it from the repository root:

```bash
PYTHONPATH=. python3 tests/example.py
```

## Quick example

```python
import cssparser


class Collector(cssparser.CSSParser):
    def __init__(self, strict=True):
        super().__init__(strict=strict)
        self.events = []

    def handle_charset(self, charset):
        self.events.append(("charset", charset))

    def handle_selector(self, selector_type, name="", predicate="", value=""):
        self.events.append(("selector", selector_type, name, predicate, value))

    def handle_declaration(self, property_name, value):
        self.events.append(("declaration", property_name, value))


parser = Collector()
parser.feed("""@charset "utf-8";

div.logo {
    color: #265581;
    top: 2px;
    border: 1px solid #265581;
    font-family: 'Arial', bold;
    font-size: 12pt;
}
""")
parser.close()

for event in parser.events:
    print(event)
```

```
('charset', '"utf-8"')
('selector', 'type', 'div', '', '')
('selector', 'class', 'logo', '', '')
('declaration', 'color', '#265581')
('declaration', 'top', '2px')
('declaration', 'border', '1px solid #265581')
('declaration', 'font-family', "'Arial', bold")
('declaration', 'font-size', '12pt')
```

`@charset` must be written exactly as `@charset ` with the trailing space required by CSS 2.1. The charset value keeps its quotes.

## Parsing model

`CSSParser(strict=True)` creates a parser. `strict` defaults to `True`.

| Method | Behavior |
| --- | --- |
| `feed(data)` | Append a `str`. Complete top-level statements (a construct ending in `;` or `}`) are parsed immediately. An unfinished statement stays in the buffer. |
| `close()` | Parse whatever remains in the buffer, as if the input had ended. |
| `reset()` | Drop the buffer and start line and column numbering again. Already delivered events are left to the subclass. |

Handlers run only for a statement that parsed successfully. A ruleset is delivered as a whole: its selectors, then its declarations. The base-class handlers do nothing, so overriding only the methods you need is enough.

Strings and comments are skipped while the parser looks for the end of a statement, so a `;` or `}` inside them does not split the input.

The extension keeps global lexer state. Use one parser at a time; it is not reentrant and not safe to share across threads.

## Handlers

| Handler | Arguments |
| --- | --- |
| `handle_charset(self, charset)` | Charset string, including the surrounding quotes. |
| `handle_selector(self, selector_type, name="", predicate="", value="")` | One simple selector. See the table below. |
| `handle_combinator(self, combinator)` | `"+"` (adjacent sibling), `">"` (child), or `" "` (descendant). |
| `handle_separator(self)` | A comma between selectors in a selector list. |
| `handle_declaration(self, property_name, value)` | Property name and its value text. `!important` is appended as `" !important"`. |

`handle_selector` arguments:

| `selector_type` | `name` | `predicate` | `value` |
| --- | --- | --- | --- |
| `"type"` | Element name, or `"*"` | `""` | `""` |
| `"class"` | Class name, without `.` | `""` | `""` |
| `"id"` | Id, without `#` | `""` | `""` |
| `"attribute"` | Attribute name | `""`, `"="`, `"~="`, or `"|="` | Attribute value. Quoted strings keep their quotes. |
| `"pseudo"` | Pseudo-class name, without `:` | `""` | Argument of `:lang()`, otherwise `""` |

Simple selectors that sit next to each other (`div.logo#brand`) are reported one after another, with no combinator between them. A combinator is reported only when one joins two compound selectors.

`@import` is accepted and produces no events. Rules inside `@media` and `@page` are reported as ordinary selectors and declarations. `@page :first` is a pseudo selector named `"first"`.

## Examples

### Selector lists and combinators

```python
css = """
h1, h2.x { color: red }
body > div + p span { color: blue }
"""
```

Events, in order:

```
selector  type h1
separator
selector  type h2
selector  class x
declaration  color  red
selector  type body
combinator  >
selector  type div
combinator  +
selector  type p
combinator  " "      # one space: p span
selector  type span
declaration  color  blue
```

### Attributes and pseudo-classes

```python
css = """
a[href] { color: black }
input[type="text"] { margin: 0 }
a[lang|="en"] { color: #abc }
div.logo#brand:hover { color: green }
:lang(en) { quotes: none }
"""
```

```
selector  type a
selector  attribute href
declaration  color  black

selector  type input
selector  attribute type  =  "text"
declaration  margin  0

selector  type a
selector  attribute lang  |=  "en"
declaration  color  #abc

selector  type div
selector  class logo
selector  id brand
selector  pseudo hover
declaration  color  green

selector  pseudo lang  value=en
declaration  quotes  none
```

An attribute with no operator, such as `[href]`, has an empty predicate and an empty value. `~=` (one of the words in a space-separated list) is reported the same way as `=`.

### Property values

Token text is joined into one string:

- words and numbers next to each other are separated by a single space
- a comma stays `", "`
- `/` stays attached to the surrounding tokens (`12pt/14pt`)
- a leading `+` or `-` stays attached to the number (`-10px`)
- `!important` becomes a trailing `" !important"`
- a function keeps its parentheses (`rgb(1, 2, 3)`)

```python
css = """
p {
    margin: -10px;
    font: italic 12pt/14pt Arial, sans-serif;
    color: red !important;
    background: rgb(1, 2, 3);
}
"""
```

```
declaration  margin      -10px
declaration  font        italic 12pt/14pt Arial, sans-serif
declaration  color       red !important
declaration  background  rgb(1, 2, 3)
```

A hex color must be 3 or 6 hexadecimal digits (`#abc`, `#265581`). Any other length raises `CSSParseError` with the message `invalid hex color` when `strict` is true.

Comments (`/* ... */`) and the HTML markers `<!--` and `-->` are ignored. An empty declaration (`color: red;;`) is skipped. The semicolon before `}` may be omitted.

### Incremental input

`feed` waits until a statement is complete.

```python
parser = Collector()
parser.feed("div { color: ")   # buffered, no events yet
parser.feed("red }\n")
parser.close()
# selector type div
# declaration color red
```

`reset()` throws away the unfinished piece and restarts the line counter at 1:

```python
parser.feed("span { color: ")
parser.reset()
parser.feed("em { color: blue }")
parser.close()
# only the em rule is reported
```

### Strict errors

With the default `strict=True`, invalid CSS raises `cssparser.CSSParseError` (also available as `cssparser.error`).

| Attribute | Meaning |
| --- | --- |
| `msg` | Short explanation. Also used as the exception text. |
| `lineno` | 1-based line number. |
| `offset` | 0-based column where the broken construct starts. |

```python
parser = cssparser.CSSParser()
try:
    parser.feed("*div { color: red }\n")
    parser.close()
except cssparser.CSSParseError as error:
    print(error.msg)      # syntax error, unexpected IDENT, expecting '{'
    print(error.lineno)   # 1
    print(error.offset)   # 1
```

`*div` is invalid in CSS 2.1 because a universal selector cannot be written immediately against a type selector. The failed statement produces no events. Statements that were already parsed on earlier `feed` calls stay delivered:

```python
parser = Collector()
parser.feed("div { color: red }\n")
try:
    parser.feed("span { color: ; }\n")
    parser.close()
except cssparser.CSSParseError as error:
    print(error.lineno)  # 2
# events still contain the div rule
```

After an error the buffer is cleared and the line cursor returns to 1, so the next `feed` starts a new stylesheet fragment.

### Skipping invalid CSS

`CSSParser(strict=False)` drops a bad ruleset or a bad declaration and continues.

```python
parser = Collector(strict=False)
parser.feed("""
*div { color: red }
p { color: #abcd; height: 10px; margin: 1px }
""")
parser.close()
```

`*div` is dropped as a whole. Inside the `p` rule, `#abcd` is an illegal color, so that declaration is dropped and `height` and `margin` are kept:

```
selector  type p
declaration  height  10px
declaration  margin  1px
```

The same thing happens inside `@media`: a bad ruleset is skipped, and later rulesets in that block are still reported. A bad declaration does not discard the rest of its ruleset.

## What the grammar accepts

Stylesheet order follows CSS 2.1: an optional `@charset`, `@import` rules, then a body of rulesets, `@media`, and `@page`.

Selectors cover type (including `*`), class, id, attributes (`=`, `~=`, `|=`), pseudo-classes, and the combinators ` `, `>`, and `+`. Declaration values cover identifiers, strings, numbers, percentages, lengths (`px`, `em`, `ex`, and the other CSS 2.1 units), angles, times, frequencies, colors, `url()`, functions, and `!important`.

## Outside this parser

The grammar stops at CSS 2.1. These constructs are syntax errors here:

- the general sibling combinator `~`
- `::` pseudo-elements
- `:not()` and other CSS3 pseudo-classes
- attribute operators `^=`, `$=`, and `*=`
- `@supports`, `@keyframes`, and `@font-face`
- `calc()`, custom properties, and nesting
- media-query features (`and`, `only`, width conditions)

Unknown dimensions such as `12turn` are syntax errors. In strict mode they fail the statement. In non-strict mode that declaration is dropped.

## Tests

```bash
python3 -m unittest tests.test_cssparser -v
```

GitHub Actions runs this on Ubuntu and macOS with Python 3.11 and 3.12.

## License

MIT. See [LICENSE](LICENSE).

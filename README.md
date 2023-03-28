Python CSSParser
======

[![CI](https://github.com/kreshikhin/cssparser/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/kreshikhin/cssparser/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![CSS 2.1](https://img.shields.io/badge/CSS-2.1-264de4)](https://www.w3.org/TR/CSS21/grammar.html)

Experimental Python module based on the [CSS 2.1 lex/yacc grammar][1].

This module defines a class CSSParser which serves as the basis for parsing CSS (Cascading Style Sheets) formatted files.

Build with flex and bison installed:

```
python3 setup.py build_ext --inplace
```

*class* cssparser.**CSSParser**(*strict=True*)

Create a parser instance. If strict is True (the default), invalid CSS results in CSSParseError exceptions. If strict is False, the parser uses heuristics to make a best guess at the intention of any invalid CSS it encounters, similar to the way most browsers do. Using strict=False is advised.

An exception is defined as well:

*exception* cssparser.**CSSParseError**

Exception raised by the CSSParser class when it encounters an error while parsing and strict is True. This exception provides three attributes: msg is a brief message explaining the error, lineno is the number of the line on which the broken construct was detected, and offset is the 0-based number of characters into the line at which the construct starts.


Example CSS Parser Application
------------------------------

As a basic example, below is a simple CSS parser that uses the CSSParser class to print out start tags, end tags, and data as they are encountered:

```python
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
```

The output will then be:

```
Encountered a charset: "utf-8"
Encountered a selector: type div  
Encountered a selector: class logo  
Encountered a declaration: background-color white
Encountered a declaration: color #265581
Encountered a declaration: position relative
Encountered a declaration: top 2px
Encountered a declaration: margin 3px
Encountered a declaration: margin-top 10px
Encountered a declaration: padding 2px
Encountered a declaration: border 1px solid #265581
Encountered a declaration: border-radius 3px
Encountered a declaration: font-family 'Arial', bold
Encountered a declaration: font-size 12pt
```

CSSParser Methods
-----------------

CSSParser instances have the following methods:

<table>
<tr>
<td>CSSParser.feed(data)</td>
<td>Feed some text to the parser. It is processed insofar as it consists of complete elements; incomplete data is buffered until more data is fed or close() is called. data must be str.</td>
</tr>
<tr>
<td>CSSParser.close()</td>
<td>Force processing of all buffered data as if it were followed by an end-of-file mark. This method may be redefined by a derived class to define additional processing at the end of the input, but the redefined version should always call the CSSParser base class method close().</td>
</tr>
<tr>
<td>CSSParser.reset()</td>
<td>Reset the instance. Loses all unprocessed data. This is called implicitly at instantiation time.
The following methods are called when data or markup elements are encountered and they are meant to be overridden in a subclass. The base class implementations do nothing.
</td>
</tr>
<tr>
<td>CSSParser.handle_charset(self, charset)</td>       
<td>This method is called to handle the charset.</td>
</tr>
<tr>
<td>CSSParser.handle_combinator(self, combinator)</td>
<td>Called with the combinator that joins compound selectors: <code>+</code>, <code>&gt;</code>, or a single space for a descendant combinator.</td>
</tr>
<tr>
<td>CSSParser.handle_separator(self)</td>
<td>Called for the comma that separates selectors in a selector list.</td>
</tr>
<tr>
<td>
CSSParser.handle_selector(self, selector_type = '', name = '', predicate = '', value = ''):
</td>
<td>
This method is called to handle the simple selector as part of a compound selector.
</td>
</tr>
<tr>
<td>
CSSParser.handle_declaration(self, property_name, value)
</td>
<td>Called for a declaration. <code>value</code> is the property value; <code>!important</code> is included when present.
</td>
</table>

[1]: http://www.w3.org/TR/CSS21/grammar.html

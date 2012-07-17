Python CSSParser
======

Experimental Python module based on [w3.org lex/yacc][1] grammar.

This module defines a class CSSParser which serves as the basis for parsing CSS (Cascading Style Sheets) formatted files.

*class* cssparser.**CSSParser**(*strict=True*)

Create a parser instance. If strict is True (the default), invalid CSS results in CSSParseError exceptions. If strict is False, the parser uses heuristics to make a best guess at the intention of any invalid CSS it encounters, similar to the way most browsers do. Using strict=False is advised.

An exception is defined as well:

*exception* cssparser.**CSSParseError**

Exception raised by the CSSParser class when it encounters an error while parsing and strict is True. This exception provides three attributes: msg is a brief message explaining the error, lineno is the number of the line on which the broken construct was detected, and offset is the number of characters into the line at which the construct starts.


Example CSS Parser Application
------------------------------

As a basic example, below is a simple CSS parser that uses the CSSParser class to print out start tags, end tags, and data as they are encountered:

```python
from cssparser import CSSParser

class MyCSSParser(CSSParser):
    def handle_charset(self, charset):
        print("Encountered a charset: ", charset)

    def handle_universal_selector(self):
        print("universal a selector:")
    
    def handle_complex_selector(self):
        print("Encountered a complex selector")
        
    def handle_compound_selector(self):
        print("Encountered a compound selector")

    def handle_simple_selector(self, selector_type = '', element = '', predicate = ''):
        print("Encountered a simple selector: ", selector_type, element, predicate)
    
    def handle_declaration(self):
        print("Encountered a declaration")
    
    def handle_property(self, name):
        print("Encountred a property", name)
        
parser = MyCSSParser(strict=False)
parser.feed('charset "utf-8";\n'
            'div{\n'
            '   color: red;'
            '}\n')
```

The output will then be:

```
Encountered a charset: utf-8
Encountered a complex selector
Encountered a compuond selector
Encountered a simple selector: type div
Encountered a declaration: color
```

CSSParser Methods
-----------------

CSSParser instances have the following methods:


CSSParser.**feed**(_data_)

> Feed some text to the parser. It is processed insofar as it consists of complete elements; incomplete data is buffered until more data is fed or close() is called. data must be str.

CSSParser.**close**()

Force processing of all buffered data as if it were followed by an end-of-file mark. This method may be redefined by a derived class to define additional processing at the end of the input, but the redefined version should always call the CSSParser base class method close().

CSSParser.**reset**()

Reset the instance. Loses all unprocessed data. This is called implicitly at instantiation time.
The following methods are called when data or markup elements are encountered and they are meant to be overridden in a subclass. The base class implementations do nothing.

CSSParser.**handle_charset**(*self, charset*)
        
This method is called to handle the charset.

CSSParser.**handle_ruleset**(*self*):

This method is called to handle the start of ruleset.

CSSParser.**handle_complex_selector**(*self*):
    
This method is called to handle the start of ruleset selectors.

CSSParser.**handle_combinator**(*self*):
    
This method is called to handle the combinator of a complex selector.
            
CSSParser.**handle_compound_selector**(*self*):
    
This method is called to handle the start of compound selector.

CSSParser.**handle_simple_selector**(*self, selector_type = '', element = '', predicate = ''*):
    
This method is called to handle the simple selector of a compound selector.

.............


[1]: http://www.w3.org/TR/CSS21/grammar.html

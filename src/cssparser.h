#include <Python.h>

#define CSSPARSER_HANDLE_CHARSET            "handle_charset"
#define CSSPARSER_HANDLE_SELECTOR           "handle_selector"
#define CSSPARSER_HANDLE_COMBINATOR         "handle_combinator"
#define CSSPARSER_HANDLE_SELECTOR_SEPARATOR "handle_selector_separator"
#define CSSPARSER_HANDLE_DECLARATION        "handle_declaration"

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
} cssparser_CSSParserObject;

extern cssparser_CSSParserObject* global_self;



#include <Python.h>

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
} cssparser_CSSParserObject;

extern cssparser_CSSParserObject* global_self;

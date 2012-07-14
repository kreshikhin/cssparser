#include "css.h"

static PyObject *CSSParserError;

static PyMethodDef CSSParserMethods[] = {
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef CSSParserModule = {
   PyModuleDef_HEAD_INIT,
   "cssparser",   /* name of module */
   NULL,          /* spam_doc,  module documentation, may be NULL */
   -1,            /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
   CSSParserMethods
};

extern cssparser_CSSParserObject* global_self = NULL;

static PyObject*
CSSParser_feed(
    cssparser_CSSParserObject* self,
    PyObject* args)
{
    // TODO: add synchronization
    extern FILE *yyin;
    extern FILE *yyout;
    extern int yy_flex_debug;
    yy_flex_debug = 0;
    yyout = NULL;
    
    global_self = self;
    char* data;
    PyArg_ParseTuple(args, "s", &data);
    yyin = fmemopen(data, strlen(data) + 1, "r");
    yyparse();
    fclose(yyin);
    yyin = NULL;
    Py_RETURN_NONE;
}

static PyMethodDef CSSParser_methods[] = {
    {"feed", (PyCFunction)CSSParser_feed, METH_VARARGS,
     "Feed the css data"
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject cssparser_CSSParserType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "cssparser.CSSParser",      /* tp_name */
    sizeof(cssparser_CSSParserObject),  /* tp_basicsize */
    0,                          /* tp_itemsize */
    0,                          /* tp_dealloc */
    0,                          /* tp_print */
    0,                          /* tp_getattr */
    0,                          /* tp_setattr */
    0,                          /* tp_reserved */
    0,                          /* tp_repr */
    0,                          /* tp_as_number */
    0,                          /* tp_as_sequence */
    0,                          /* tp_as_mapping */
    0,                          /* tp_hash  */
    0,                          /* tp_call */
    0,                          /* tp_str */
    0,                          /* tp_getattro */
    0,                          /* tp_setattro */
    0,                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,    /* tp_flags */
    "CSSParser object",         /* tp_doc */
    0,                          /* tp_traverse */
    0,                          /* tp_clear */
    0,                          /* tp_richcompare */
    0,                          /* tp_weaklistoffset */
    0,                          /* tp_iter */
    0,                          /* tp_iternext */
    CSSParser_methods,          /* tp_methods */
    0,                          /* tp_members */
    0,                          /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    0,                          /* tp_dictoffset */
    0,                          /* tp_init */
    0,                          /* tp_alloc */
    0,                          /* tp_new */
};

PyMODINIT_FUNC
PyInit_cssparser(void)
{
    PyObject *m;

    cssparser_CSSParserType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&cssparser_CSSParserType) < 0)
        return NULL;

    m = PyModule_Create(&CSSParserModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&cssparser_CSSParserType);
    PyModule_AddObject(m, "CSSParser", (PyObject *)&cssparser_CSSParserType);
    
    CSSParserError = PyErr_NewException("cssparser.error", NULL, NULL);
    Py_INCREF(CSSParserError);
    PyModule_AddObject(m, "error", CSSParserError);
    return m;
}



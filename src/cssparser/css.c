#include <Python.h>

static PyObject *CSSParserError;

static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    if (sts < 0) {
        PyErr_SetString(CSSParserError, "System command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);
}

static PyMethodDef CSSParserMethods[] = {
    {"system",  spam_system, METH_VARARGS, "Execute a shell command."},
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

/// define new type for CSSParser
typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
} cssparser_CSSParserObject;

static PyObject*
CSSParser_feed(
    cssparser_CSSParserObject* self,
    PyObject* args)
{
    printf("called feed\n");
    PyObject* data;
    PyArg_UnpackTuple(args, "s", 1, 1, &data);
    printf("py unicode object size: %i\n", PyUnicode_GetSize(data));
    printf("py unicode object: %s\n", PyUnicode_AsUnicode(data));
    PyObject_CallMethod((PyObject*)self, "handle_charset", "s", "UTF-8");
    Py_RETURN_NONE;
}

static PyObject*
CSSParser_handle_charset(
    cssparser_CSSParserObject* self,
    PyObject* args)
{
    Py_RETURN_NONE;
}


static PyMethodDef CSSParser_methods[] = {
    {"feed", (PyCFunction)CSSParser_feed, METH_VARARGS,
     "Feed the css data"
    },
    {"handle_charset", (PyCFunction)CSSParser_handle_charset, METH_VARARGS,
     "Callback method"
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject cssparser_CSSParserType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "cssparser.CSSParser",             /* tp_name */
    sizeof(cssparser_CSSParserObject), /* tp_basicsize */
    0,                         /* tp_itemsize */
    0,                         /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,        /* tp_flags */
    "CSSParser object",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    CSSParser_methods,             /* tp_methods */
    0,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,      /* tp_init */
    0,                         /* tp_alloc */
    0,                 /* tp_new */
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

int
main(int argc, char *argv[])
{
    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("cssparser", PyInit_cssparser);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName((wchar_t*)argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("cssparser");
}



#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cssparser.h"
#include "y.tab.h"
/* Bison's whitespace token is a one-letter macro. */
#undef S

typedef struct yy_buffer_state* YY_BUFFER_STATE;
extern int yyparse(void);
extern YY_BUFFER_STATE yy_scan_bytes(const char* bytes, int length);
extern void yy_delete_buffer(YY_BUFFER_STATE buffer);

#define CSS_MARK_MAX 64
#define CSS_ERROR_MAX 768

typedef enum {
    CSS_EV_CHARSET = 1,
    CSS_EV_SELECTOR,
    CSS_EV_COMBINATOR,
    CSS_EV_SEPARATOR,
    CSS_EV_DECLARATION
} CssEventKind;

typedef struct {
    CssEventKind kind;
    char* a;
    char* b;
    char* c;
    char* d;
} CssEvent;

struct CssEventList {
    CssEvent* items;
    int count;
    int cap;
    struct CssEventList* next_live;
};

typedef struct {
    PyObject_HEAD
    int strict;
    char* buffer;
    size_t buffer_len;
    size_t buffer_cap;
    int line_cursor;
    int column_cursor;
} CSSParserObject;

typedef struct CssArenaBlock {
    struct CssArenaBlock* next;
    size_t used;
    size_t cap;
    char* data;
} CssArenaBlock;

int css_line = 1;
int css_column = 0;
int css_strict = 1;

static int css_has_error = 0;
static int css_oom = 0;
static char css_error_message[CSS_ERROR_MAX];
static int css_error_line = 1;
static int css_error_column = 0;

static CssArenaBlock* css_arena = NULL;
static CssEventList* css_live_lists = NULL;
static CssEventList css_pending;
static int css_marks[CSS_MARK_MAX];
static int css_mark_sp = 0;

static PyObject* CSSParseError = NULL;

static void css_reset_memory(void) {
    while (css_live_lists) {
        CssEventList* next = css_live_lists->next_live;
        free(css_live_lists->items);
        free(css_live_lists);
        css_live_lists = next;
    }
    free(css_pending.items);
    css_pending.items = NULL;
    css_pending.count = 0;
    css_pending.cap = 0;
    css_pending.next_live = NULL;
    css_mark_sp = 0;

    while (css_arena) {
        CssArenaBlock* next = css_arena->next;
        free(css_arena->data);
        free(css_arena);
        css_arena = next;
    }
}

void css_advance_pos(int* line, int* column, const char* text, size_t length) {
    size_t i;
    if (!line || !column || !text) return;
    for (i = 0; i < length; i++) {
        char c = text[i];
        if (c == '\n' || c == '\f') {
            (*line)++;
            *column = 0;
        } else if (c == '\r') {
            (*line)++;
            *column = 0;
            if (i + 1 < length && text[i + 1] == '\n') i++;
        } else {
            (*column)++;
        }
    }
}

static void* css_arena_alloc(size_t size) {
    CssArenaBlock* block;
    void* ptr;
    if (size == 0) size = 1;
    size = (size + 7u) & ~((size_t)7u);
    if (!css_arena || css_arena->used + size > css_arena->cap) {
        size_t cap = 8192;
        if (size > cap) cap = size;
        block = (CssArenaBlock*)malloc(sizeof(CssArenaBlock));
        if (!block) {
            css_oom = 1;
            return NULL;
        }
        block->data = (char*)malloc(cap);
        if (!block->data) {
            free(block);
            css_oom = 1;
            return NULL;
        }
        block->cap = cap;
        block->used = 0;
        block->next = css_arena;
        css_arena = block;
    }
    ptr = css_arena->data + css_arena->used;
    css_arena->used += size;
    return ptr;
}

char* css_arena_copy(const char* text, size_t length) {
    char* out = (char*)css_arena_alloc(length + 1);
    if (!out) return NULL;
    if (length && text) memcpy(out, text, length);
    out[length] = '\0';
    return out;
}

char* css_arena_str(const char* text) {
    if (!text) text = "";
    return css_arena_copy(text, strlen(text));
}

static char* css_join_parts(const char* a, const char* b, const char* c) {
    size_t na, nb, nc;
    char* out;
    if (!a) a = "";
    if (!b) b = "";
    if (!c) c = "";
    na = strlen(a);
    nb = strlen(b);
    nc = strlen(c);
    out = (char*)css_arena_alloc(na + nb + nc + 1);
    if (!out) return NULL;
    memcpy(out, a, na);
    memcpy(out + na, b, nb);
    memcpy(out + na + nb, c, nc);
    out[na + nb + nc] = '\0';
    return out;
}

char* css_join2(const char* left, const char* right) {
    return css_join_parts(left, right, "");
}

char* css_join3(const char* left, const char* mid, const char* right) {
    return css_join_parts(left, mid, right);
}

char* css_func_name(const char* function_token) {
    size_t length = function_token ? strlen(function_token) : 0;
    if (length && function_token[length - 1] == '(') length--;
    return css_arena_copy(function_token ? function_token : "", length);
}

int css_valid_hexcolor(const char* text) {
    size_t length, i;
    if (!text || text[0] != '#') return 0;
    length = strlen(text) - 1;
    if (length != 3 && length != 6) return 0;
    for (i = 1; text[i] != '\0'; i++) {
        char c = text[i];
        int hex = (c >= '0' && c <= '9') ||
                  (c >= 'a' && c <= 'f') ||
                  (c >= 'A' && c <= 'F');
        if (!hex) return 0;
    }
    return 1;
}

void css_fail_at(const char* message, int line, int column) {
    if (css_has_error) return;
    css_has_error = 1;
    if (!message || !message[0]) message = "invalid CSS syntax";
    snprintf(css_error_message, sizeof css_error_message, "%s", message);
    css_error_line = line > 0 ? line : 1;
    css_error_column = column >= 0 ? column : 0;
}

static int css_list_push(CssEventList* list, CssEvent event) {
    if (!list) {
        css_oom = 1;
        return -1;
    }
    if (list->count >= list->cap) {
        int cap = list->cap > 0 ? list->cap * 2 : 8;
        CssEvent* items = (CssEvent*)realloc(list->items, (size_t)cap * sizeof(CssEvent));
        if (!items) {
            css_oom = 1;
            return -1;
        }
        list->items = items;
        list->cap = cap;
    }
    list->items[list->count++] = event;
    return 0;
}

CssEventList* css_list_new(void) {
    CssEventList* list = (CssEventList*)calloc(1, sizeof(CssEventList));
    if (!list) {
        css_oom = 1;
        return NULL;
    }
    list->next_live = css_live_lists;
    css_live_lists = list;
    return list;
}

int css_list_add_selector(CssEventList* list, const char* type, const char* name,
                          const char* predicate, const char* value) {
    CssEvent event;
    event.kind = CSS_EV_SELECTOR;
    event.a = (char*)(type ? type : "");
    event.b = (char*)(name ? name : "");
    event.c = (char*)(predicate ? predicate : "");
    event.d = (char*)(value ? value : "");
    return css_list_push(list, event);
}

int css_list_add_combinator(CssEventList* list, const char* combinator) {
    CssEvent event;
    event.kind = CSS_EV_COMBINATOR;
    event.a = (char*)(combinator ? combinator : "");
    event.b = NULL;
    event.c = NULL;
    event.d = NULL;
    return css_list_push(list, event);
}

int css_list_add_separator(CssEventList* list) {
    CssEvent event;
    event.kind = CSS_EV_SEPARATOR;
    event.a = NULL;
    event.b = NULL;
    event.c = NULL;
    event.d = NULL;
    return css_list_push(list, event);
}

CssEventList* css_list_concat(CssEventList* left, CssEventList* right) {
    int i;
    if (!left) return right;
    if (!right) return left;
    for (i = 0; i < right->count; i++) {
        if (css_list_push(left, right->items[i]) < 0) return NULL;
    }
    return left;
}

static int css_pending_push(CssEvent event) {
    return css_list_push(&css_pending, event);
}

int css_pending_add(CssEventList* list) {
    int i;
    if (!list) return 0;
    for (i = 0; i < list->count; i++) {
        if (css_pending_push(list->items[i]) < 0) return -1;
    }
    return 0;
}

int css_push_charset(const char* charset) {
    CssEvent event;
    event.kind = CSS_EV_CHARSET;
    event.a = (char*)(charset ? charset : "");
    event.b = NULL;
    event.c = NULL;
    event.d = NULL;
    return css_pending_push(event);
}

int css_push_declaration(const char* property, const char* value) {
    CssEvent event;
    event.kind = CSS_EV_DECLARATION;
    event.a = (char*)(property ? property : "");
    event.b = (char*)(value ? value : "");
    event.c = NULL;
    event.d = NULL;
    return css_pending_push(event);
}

int css_mark(void) {
    if (css_mark_sp >= CSS_MARK_MAX) {
        css_oom = 1;
        return -1;
    }
    css_marks[css_mark_sp++] = css_pending.count;
    return 0;
}

void css_commit(void) {
    if (css_mark_sp > 0) css_mark_sp--;
}

void css_rollback(void) {
    int mark;
    if (css_mark_sp <= 0) return;
    mark = css_marks[--css_mark_sp];
    if (mark < 0) mark = 0;
    if (mark > css_pending.count) mark = css_pending.count;
    css_pending.count = mark;
}

static void css_prepare_parse(int strict, int line, int column) {
    css_reset_memory();
    css_strict = strict ? 1 : 0;
    css_line = line > 0 ? line : 1;
    css_column = column >= 0 ? column : 0;
    css_has_error = 0;
    css_oom = 0;
    css_error_message[0] = '\0';
    css_error_line = css_line;
    css_error_column = css_column;
    yylloc.first_line = css_line;
    yylloc.first_column = css_column;
    yylloc.last_line = css_line;
    yylloc.last_column = css_column;
}

static void css_raise_parse_error(void) {
    const char* message = css_error_message[0] ? css_error_message : "invalid CSS syntax";
    PyObject* exc = PyObject_CallFunction(CSSParseError, "s", message);
    PyObject* py_message;
    PyObject* py_line;
    PyObject* py_column;
    if (!exc) return;
    py_message = PyUnicode_FromString(message);
    py_line = PyLong_FromLong(css_error_line);
    py_column = PyLong_FromLong(css_error_column);
    if (py_message) PyObject_SetAttrString(exc, "msg", py_message);
    if (py_line) PyObject_SetAttrString(exc, "lineno", py_line);
    if (py_column) PyObject_SetAttrString(exc, "offset", py_column);
    Py_XDECREF(py_message);
    Py_XDECREF(py_line);
    Py_XDECREF(py_column);
    PyErr_SetObject(CSSParseError, exc);
    Py_DECREF(exc);
}

static int css_emit_all(PyObject* self) {
    int i;
    for (i = 0; i < css_pending.count; i++) {
        CssEvent* event = &css_pending.items[i];
        PyObject* result = NULL;
        switch (event->kind) {
        case CSS_EV_CHARSET:
            result = PyObject_CallMethod(self, "handle_charset", "s", event->a ? event->a : "");
            break;
        case CSS_EV_SELECTOR:
            result = PyObject_CallMethod(
                self, "handle_selector", "ssss",
                event->a ? event->a : "",
                event->b ? event->b : "",
                event->c ? event->c : "",
                event->d ? event->d : "");
            break;
        case CSS_EV_COMBINATOR:
            result = PyObject_CallMethod(self, "handle_combinator", "s", event->a ? event->a : "");
            break;
        case CSS_EV_SEPARATOR:
            result = PyObject_CallMethod(self, "handle_separator", NULL);
            break;
        case CSS_EV_DECLARATION:
            result = PyObject_CallMethod(
                self, "handle_declaration", "ss",
                event->a ? event->a : "",
                event->b ? event->b : "");
            break;
        default:
            break;
        }
        if (event->kind != CSS_EV_CHARSET &&
            event->kind != CSS_EV_SELECTOR &&
            event->kind != CSS_EV_COMBINATOR &&
            event->kind != CSS_EV_SEPARATOR &&
            event->kind != CSS_EV_DECLARATION) {
            continue;
        }
        if (!result) return -1;
        Py_DECREF(result);
    }
    return 0;
}

/* End of the next top-level statement, or 0 when the tail is still incomplete. */
static size_t css_statement_end(const char* text, size_t length) {
    size_t i;
    int depth = 0;
    int in_comment = 0;
    char quote = 0;
    int escape = 0;

    for (i = 0; i < length; i++) {
        char c = text[i];
        if (in_comment) {
            if (c == '*' && i + 1 < length && text[i + 1] == '/') {
                in_comment = 0;
                i++;
            }
            continue;
        }
        if (quote) {
            if (escape) {
                escape = 0;
                continue;
            }
            if (c == '\\') {
                escape = 1;
                continue;
            }
            if (c == '\n' || c == '\r' || c == '\f') {
                quote = 0;
                continue;
            }
            if (c == quote) quote = 0;
            continue;
        }
        if (c == '/' && i + 1 < length && text[i + 1] == '*') {
            in_comment = 1;
            i++;
            continue;
        }
        if (c == '"' || c == '\'') {
            quote = c;
            continue;
        }
        if (c == '{') {
            depth++;
        } else if (c == '}') {
            if (depth > 0) depth--;
            if (depth == 0) return i + 1;
        } else if (c == ';' && depth == 0) {
            return i + 1;
        }
    }
    return 0;
}

static int css_parse_chunk(CSSParserObject* self, const char* data, size_t length) {
    YY_BUFFER_STATE buffer;
    int rc;

    if (length == 0) return 0;
    if (length > (size_t)2147483647) {
        PyErr_SetString(PyExc_OverflowError, "CSS input is too large");
        return -1;
    }

    css_prepare_parse(self->strict, self->line_cursor, self->column_cursor);
    buffer = yy_scan_bytes(data, (int)length);
    if (!buffer) {
        css_reset_memory();
        PyErr_NoMemory();
        return -1;
    }
    rc = yyparse();
    yy_delete_buffer(buffer);

    while (css_mark_sp > 0) css_rollback();

    if (css_oom) {
        css_reset_memory();
        PyErr_NoMemory();
        return -1;
    }
    if (rc != 0) {
        if (self->strict) css_raise_parse_error();
        css_reset_memory();
        return self->strict ? -1 : 0;
    }
    if (css_emit_all((PyObject*)self) < 0) {
        css_reset_memory();
        return -1;
    }
    css_reset_memory();
    return 0;
}

static int css_buffer_append(CSSParserObject* self, const char* data, size_t length) {
    size_t needed;
    size_t cap;
    char* grown;
    if (length == 0) return 0;
    if (length > (size_t)-1 - self->buffer_len - 1) {
        PyErr_NoMemory();
        return -1;
    }
    needed = self->buffer_len + length + 1;
    if (needed > self->buffer_cap) {
        cap = self->buffer_cap ? self->buffer_cap : 128;
        while (cap < needed) {
            if (cap > ((size_t)-1) / 2) {
                PyErr_NoMemory();
                return -1;
            }
            cap *= 2;
        }
        grown = (char*)realloc(self->buffer, cap);
        if (!grown) {
            PyErr_NoMemory();
            return -1;
        }
        self->buffer = grown;
        self->buffer_cap = cap;
    }
    memcpy(self->buffer + self->buffer_len, data, length);
    self->buffer_len += length;
    self->buffer[self->buffer_len] = '\0';
    return 0;
}

static void css_buffer_clear(CSSParserObject* self) {
    free(self->buffer);
    self->buffer = NULL;
    self->buffer_len = 0;
    self->buffer_cap = 0;
}

static void css_buffer_consume(CSSParserObject* self, size_t length) {
    if (length >= self->buffer_len) {
        self->buffer_len = 0;
        if (self->buffer) self->buffer[0] = '\0';
        return;
    }
    memmove(self->buffer, self->buffer + length, self->buffer_len - length);
    self->buffer_len -= length;
    self->buffer[self->buffer_len] = '\0';
}

static int css_parse_available(CSSParserObject* self, int force) {
    while (self->buffer && self->buffer_len > 0) {
        size_t prefix = force ? self->buffer_len : css_statement_end(self->buffer, self->buffer_len);
        if (prefix == 0) break;
        if (css_parse_chunk(self, self->buffer, prefix) < 0) {
            css_buffer_clear(self);
            self->line_cursor = 1;
            self->column_cursor = 0;
            return -1;
        }
        css_advance_pos(&self->line_cursor, &self->column_cursor, self->buffer, prefix);
        css_buffer_consume(self, prefix);
    }
    return 0;
}

static PyObject* CSSParser_feed(CSSParserObject* self, PyObject* args) {
    const char* data;
    Py_ssize_t length;
    if (!PyArg_ParseTuple(args, "s#", &data, &length)) return NULL;
    if (length < 0) {
        PyErr_SetString(PyExc_ValueError, "CSS input length is invalid");
        return NULL;
    }
    if (css_buffer_append(self, data, (size_t)length) < 0) return NULL;
    if (css_parse_available(self, 0) < 0) return NULL;
    Py_RETURN_NONE;
}

static PyObject* CSSParser_close(CSSParserObject* self, PyObject* Py_UNUSED(ignored)) {
    if (css_parse_available(self, 1) < 0) return NULL;
    Py_RETURN_NONE;
}

static PyObject* CSSParser_reset(CSSParserObject* self, PyObject* Py_UNUSED(ignored)) {
    css_buffer_clear(self);
    self->line_cursor = 1;
    self->column_cursor = 0;
    Py_RETURN_NONE;
}

static PyObject* CSSParser_noop(PyObject* self, PyObject* args) {
    (void)self;
    (void)args;
    Py_RETURN_NONE;
}

static PyMethodDef CSSParser_methods[] = {
    {"feed", (PyCFunction)CSSParser_feed, METH_VARARGS, "Feed CSS text. Complete rules are parsed immediately."},
    {"close", (PyCFunction)CSSParser_close, METH_NOARGS, "Parse any buffered tail as the end of the stylesheet."},
    {"reset", (PyCFunction)CSSParser_reset, METH_NOARGS, "Drop buffered input and restart line numbering."},
    {"handle_charset", CSSParser_noop, METH_VARARGS, "Called with the charset string, including quotes."},
    {"handle_selector", CSSParser_noop, METH_VARARGS, "Called for one simple selector."},
    {"handle_combinator", CSSParser_noop, METH_VARARGS, "Called with '+', '>' or a space."},
    {"handle_separator", CSSParser_noop, METH_NOARGS, "Called for a comma between selectors."},
    {"handle_declaration", CSSParser_noop, METH_VARARGS, "Called with a property name and its value."},
    {NULL, NULL, 0, NULL}
};

static void CSSParser_dealloc(PyObject* self) {
    CSSParserObject* parser = (CSSParserObject*)self;
    free(parser->buffer);
    Py_TYPE(self)->tp_free(self);
}

static PyObject* CSSParser_new(PyTypeObject* type, PyObject* args, PyObject* kwargs) {
    CSSParserObject* self;
    (void)args;
    (void)kwargs;
    self = (CSSParserObject*)type->tp_alloc(type, 0);
    if (!self) return NULL;
    self->strict = 1;
    self->buffer = NULL;
    self->buffer_len = 0;
    self->buffer_cap = 0;
    self->line_cursor = 1;
    self->column_cursor = 0;
    return (PyObject*)self;
}

static int CSSParser_init(PyObject* self, PyObject* args, PyObject* kwargs) {
    static char* keywords[] = {"strict", NULL};
    int strict = 1;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|p", keywords, &strict)) return -1;
    ((CSSParserObject*)self)->strict = strict ? 1 : 0;
    return 0;
}

static PyType_Slot CSSParser_slots[] = {
    {Py_tp_doc,
     "CSS 2.1 stylesheet parser.\n\n"
     "CSSParser(strict=True) raises CSSParseError when a construct is invalid.\n"
     "With strict=False, invalid selectors, at-rules and declarations are skipped."},
    {Py_tp_methods, CSSParser_methods},
    {Py_tp_init, (void*)CSSParser_init},
    {Py_tp_new, (void*)CSSParser_new},
    {Py_tp_dealloc, (void*)CSSParser_dealloc},
    {0, NULL}
};

static PyType_Spec CSSParser_spec = {
    "cssparser.CSSParser",
    sizeof(CSSParserObject),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    CSSParser_slots
};

static PyMethodDef module_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cssparser_module = {
    PyModuleDef_HEAD_INIT,
    "cssparser",
    "CSS 2.1 parser based on the W3C lex/yacc grammar.",
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_cssparser(void) {
    PyObject* module;
    PyObject* type;

    module = PyModule_Create(&cssparser_module);
    if (!module) return NULL;

    type = PyType_FromSpec(&CSSParser_spec);
    if (!type) {
        Py_DECREF(module);
        return NULL;
    }
    if (PyModule_AddObjectRef(module, "CSSParser", type) < 0) {
        Py_DECREF(type);
        Py_DECREF(module);
        return NULL;
    }
    Py_DECREF(type);

    CSSParseError = PyErr_NewException("cssparser.CSSParseError", NULL, NULL);
    if (!CSSParseError) {
        Py_DECREF(module);
        return NULL;
    }
    if (PyModule_AddObjectRef(module, "CSSParseError", CSSParseError) < 0 ||
        PyModule_AddObjectRef(module, "error", CSSParseError) < 0) {
        Py_DECREF(CSSParseError);
        Py_DECREF(module);
        return NULL;
    }
    return module;
}

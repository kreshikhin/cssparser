#ifndef CSSPARSER_H
#define CSSPARSER_H

#include <stddef.h>

typedef struct CssEventList CssEventList;

/* 1-based line, 0-based column, matching HTMLParseError. */
void css_advance_pos(int* line, int* column, const char* text, size_t length);

char* css_arena_copy(const char* text, size_t length);
char* css_arena_str(const char* text);
char* css_join2(const char* left, const char* right);
char* css_join3(const char* left, const char* mid, const char* right);
char* css_func_name(const char* function_token);
int css_valid_hexcolor(const char* text);

CssEventList* css_list_new(void);
int css_list_add_selector(CssEventList* list, const char* type, const char* name,
                          const char* predicate, const char* value);
int css_list_add_combinator(CssEventList* list, const char* combinator);
int css_list_add_separator(CssEventList* list);
CssEventList* css_list_concat(CssEventList* left, CssEventList* right);

int css_pending_add(CssEventList* list);
int css_push_charset(const char* charset);
int css_push_declaration(const char* property, const char* value);
int css_mark(void);
void css_commit(void);
void css_rollback(void);

void css_fail_at(const char* message, int line, int column);

extern int css_line;
extern int css_column;
extern int css_strict;

#endif

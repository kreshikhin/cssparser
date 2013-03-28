%{
#include "cssparser.h"

int yylex(void);
int yyerror(const char* message);
%}

%error-verbose
%locations
/* ';' continues a declaration; another term continues an expr. */
%expect 2

%union {
    char* string;
    struct CssEventList* list;
}

%token <string> ANGLE
%token <string> DASHMATCH
%token <string> DIMENSION
%token <string> EMS
%token <string> EXS
%token <string> FREQ
%token <string> FUNCTION
%token <string> HASH
%token <string> IDENT
%token <string> INCLUDES
%token <string> LENGTH
%token <string> NUMBER
%token <string> PERCENTAGE
%token <string> STRING
%token <string> TIME
%token <string> URI

%token BAD_STRING BAD_URI
%token CHARSET_SYM
%token IMPORT_SYM IMPORTANT_SYM MEDIA_SYM PAGE_SYM
%token S

%type <string> attrib_eq attrib_value expr function hexcolor property term term_numeral
%type <list> attribute_selector class_selector complex_selector compound_selector
%type <list> id_selector pseudo_selector selector_list simple_selector type_selector

%start stylesheet

%%

stylesheet
    : charset comments import_block body
    ;

charset
    : /* empty */
    | CHARSET_SYM STRING ';'
        {
            if (css_push_charset($2) < 0) YYABORT;
        }
    ;

comments
    : /* empty */
    | comments S
    ;

import_block
    : /* empty */
    | import_block import
    ;

import
    : IMPORT_SYM spaces STRING spaces ';' spaces
        { (void)$3; }
    | IMPORT_SYM spaces URI spaces ';' spaces
        { (void)$3; }
    | IMPORT_SYM spaces STRING spaces media_list ';' spaces
        { (void)$3; }
    | IMPORT_SYM spaces URI spaces media_list ';' spaces
        { (void)$3; }
    ;

media
    : MEDIA_SYM spaces media_list '{' spaces rulesets '}' spaces
    ;

rulesets
    : /* empty */
    | rulesets ruleset
    ;

media_list
    : medium
    | media_list ',' spaces medium
    ;

medium
    : IDENT spaces
        { (void)$1; }
    ;

page
    : PAGE_SYM spaces ':' IDENT spaces
        {
            struct CssEventList* selectors = css_list_new();
            if (!selectors || css_list_add_selector(selectors, "pseudo", $4, "", "") < 0) YYABORT;
            if (css_mark() < 0 || css_pending_add(selectors) < 0) YYABORT;
        }
        '{' spaces declarations '}' spaces
        { css_commit(); }
    | PAGE_SYM spaces
        {
            if (css_mark() < 0) YYABORT;
        }
        '{' spaces declarations '}' spaces
        { css_commit(); }
    ;

body
    : /* empty */
    | body ruleset
    | body media
    | body page
    ;

ruleset
    : selector_list
        {
            if (css_mark() < 0 || css_pending_add($1) < 0) YYABORT;
        }
        '{' spaces declarations '}' spaces
        { css_commit(); }
    ;

selector_list
    : complex_selector
    | selector_list ',' spaces complex_selector
        {
            if (css_list_add_separator($1) < 0) YYABORT;
            $$ = css_list_concat($1, $4);
            if (!$$) YYABORT;
        }
    ;

complex_selector
    : compound_selector
    | complex_selector '+' spaces compound_selector
        {
            if (css_list_add_combinator($1, "+") < 0) YYABORT;
            $$ = css_list_concat($1, $4);
            if (!$$) YYABORT;
        }
    | complex_selector '>' spaces compound_selector
        {
            if (css_list_add_combinator($1, ">") < 0) YYABORT;
            $$ = css_list_concat($1, $4);
            if (!$$) YYABORT;
        }
    | complex_selector S compound_selector
        {
            if (css_list_add_combinator($1, " ") < 0) YYABORT;
            $$ = css_list_concat($1, $3);
            if (!$$) YYABORT;
        }
    | complex_selector S
        { $$ = $1; }
    ;

compound_selector
    : type_selector
    | simple_selector
    | compound_selector simple_selector
        {
            $$ = css_list_concat($1, $2);
            if (!$$) YYABORT;
        }
    ;

simple_selector
    : attribute_selector
    | class_selector
    | id_selector
    | pseudo_selector
    ;

type_selector
    : IDENT
        {
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "type", $1, "", "") < 0) YYABORT;
        }
    | '*'
        {
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "type", "*", "", "") < 0) YYABORT;
        }
    ;

class_selector
    : '.' IDENT
        {
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "class", $2, "", "") < 0) YYABORT;
        }
    ;

id_selector
    : HASH
        {
            const char* name = ($1 && $1[0] == '#') ? $1 + 1 : ($1 ? $1 : "");
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "id", name, "", "") < 0) YYABORT;
        }
    ;

attribute_selector
    : '[' spaces IDENT spaces ']'
        {
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "attribute", $3, "", "") < 0) YYABORT;
        }
    | '[' spaces IDENT spaces attrib_eq spaces attrib_value spaces ']'
        {
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "attribute", $3, $5, $7) < 0) YYABORT;
        }
    ;

attrib_eq
    : '='       { $$ = (char*)"="; }
    | INCLUDES  { $$ = $1; }
    | DASHMATCH { $$ = $1; }
    ;

attrib_value
    : IDENT  { $$ = $1; }
    | STRING { $$ = $1; }
    ;

pseudo_selector
    : ':' IDENT
        {
            $$ = css_list_new();
            if (!$$ || css_list_add_selector($$, "pseudo", $2, "", "") < 0) YYABORT;
        }
    | ':' FUNCTION spaces IDENT spaces ')'
        {
            char* name = css_func_name($2);
            $$ = css_list_new();
            if (!name || !$$ || css_list_add_selector($$, "pseudo", name, "", $4) < 0) YYABORT;
        }
    | ':' FUNCTION spaces ')'
        {
            char* name = css_func_name($2);
            $$ = css_list_new();
            if (!name || !$$ || css_list_add_selector($$, "pseudo", name, "", "") < 0) YYABORT;
        }
    ;

declarations
    : /* empty */
    | declarations declaration_item
    ;

declaration_item
    : declaration ';' spaces
    | declaration
    | ';' spaces
    ;

declaration
    : property ':' spaces expr
        {
            if (css_push_declaration($1, $4) < 0) YYABORT;
        }
    | property ':' spaces expr IMPORTANT_SYM spaces
        {
            char* value = css_join2($4, " !important");
            if (!value || css_push_declaration($1, value) < 0) YYABORT;
        }
    ;

property
    : IDENT spaces
        { $$ = $1; }
    ;

expr
    : term
        { $$ = $1; }
    | expr '/' spaces term
        {
            $$ = css_join3($1, "/", $4);
            if (!$$) YYABORT;
        }
    | expr ',' spaces term
        {
            $$ = css_join3($1, ", ", $4);
            if (!$$) YYABORT;
        }
    | expr term
        {
            $$ = css_join3($1, " ", $2);
            if (!$$) YYABORT;
        }
    ;

term
    : '-' term_numeral spaces
        {
            $$ = css_join2("-", $2);
            if (!$$) YYABORT;
        }
    | '+' term_numeral spaces
        {
            $$ = css_join2("+", $2);
            if (!$$) YYABORT;
        }
    | term_numeral spaces
        { $$ = $1; }
    | STRING spaces
        { $$ = $1; }
    | IDENT spaces
        { $$ = $1; }
    | URI spaces
        { $$ = $1; }
    | hexcolor
    | function
    ;

term_numeral
    : NUMBER
    | PERCENTAGE
    | LENGTH
    | EMS
    | EXS
    | ANGLE
    | TIME
    | FREQ
    ;

function
    : FUNCTION spaces expr ')' spaces
        {
            $$ = css_join3($1, $3, ")");
            if (!$$) YYABORT;
        }
    ;

hexcolor
    : HASH spaces
        { $$ = $1; }
    ;

spaces
    : /* empty */
    | spaces S
    ;

%%

int yyerror(const char* message)
{
    int line = css_line > 0 ? css_line : 1;
    int column = css_column >= 0 ? css_column : 0;
    if (yylloc.first_line > 0) {
        line = yylloc.first_line;
        column = yylloc.first_column;
    }
    css_fail_at(message && message[0] ? message : "invalid CSS syntax", line, column);
    return 0;
}

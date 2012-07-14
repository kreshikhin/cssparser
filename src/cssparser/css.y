
%{
#include <stdio.h>
#include "css.h"
%}

%start stylesheet

%union{
    char* string;
}

%token <string> ANGLE
%token <string> BAD_STRING
%token <string> BAD_URI
%token CDC CDO CHARSET_SYM
%token DASHMATCH DIMENSION
%token EMS EXS
%token S
%token <string> STRING
%token <string> FREQ
%token FUNCTION
%token <string> HASH
%token <string> IDENT
%token INCLUDES IMPORT_SYM IMPORTANT_SYM
%token <string> LENGTH
%token MEDIA_SYM
%token <string> NUMBER
%token PAGE_SYM
%token <string> PERCENTAGE 
%token <string> TIME
%token <string> URI

%type <string> type_selector
%type <string> id_selector
%type <string> class_selector

%%

stylesheet // : [ CHARSET_SYM STRING ';' ]?
           //   [S|CDO|CDC]* [ import [ CDO S* | CDC S* ]* ]*
           //   [ [ ruleset | media | page ] [ CDO S* | CDC S* ]* ]* ;
    : charset comments import_block body
;

charset
    :
    | CHARSET_SYM STRING ';'
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_charset", "s", $2);
    }
;

comments
    :
    | comments S
    | comments CDO
    | comments CDC
;

import_block
    :
    | import subcomments
;

body
    :
    | body ruleset subcomments
    | body media subcomments
    | body page subcomments
;

subcomments
    :
    | subcomments CDO spaces
    | subcomments CDC spaces
;

import // : IMPORT_SYM S* [STRING|URI] S* media_list? ';' S* ;
    : IMPORT_SYM spaces STRING spaces media_list ';' spaces
    | IMPORT_SYM spaces URI spaces media_list ';' spaces
    | IMPORT_SYM spaces STRING spaces ';' spaces
    | IMPORT_SYM spaces URI spaces ';' spaces
;
    
media // : MEDIA_SYM S* media_list '{' S* ruleset* '}' S* ;
    : MEDIA_SYM spaces media_list '{' spaces rulesets '}' spaces
;

rulesets
    :
    | rulesets ruleset
;

media_list // : medium [ COMMA S* medium]* ;
    : medium
    | media_list ',' spaces medium
;

medium // : IDENT S* ;
    : IDENT spaces
;

page // : PAGE_SYM S* pseudo_page?
     //   '{' S* declaration? [ ';' S* declaration? ]* '}' S* ;
    : PAGE_SYM spaces pseudo_page '{' page_declarations '}' spaces
    | PAGE_SYM spaces '{' page_declarations '}' spaces
;

page_declarations
    : spaces declaration
    | spaces
    | page_declarations ';' spaces declaration
    | page_declarations ';' spaces
;

pseudo_page // : ':' IDENT S* ;
    : ':' IDENT spaces
;

operator // : '/' S* | ',' S* ;
    : '/' spaces
    | ',' spaces
;

combinator // : '+' S* | '>' S* ;
    : '+' spaces
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_combinator", "s", "+");
    }
    | '>' spaces
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_combinator", "s", ">");
    }
;

unary_operator // : '-' | '+' ;
    : '-'
    | '+'
;

property // : IDENT S* ;
    : IDENT spaces
;

ruleset // : selector [ ',' S* selector ]* '{' S* declaration? [ ';' S* declaration? ]* '}' S* ;
    : selector_list '{' spaces declarations '}' spaces
    | selector_list '{' spaces '}' spaces
;

selector_list
    : complex_selector
    | selector_list ',' spaces complex_selector
;

declarations
    : declaration
    | declarations ';' spaces declaration
    | declarations ';' spaces
;

complex_selector // : simple_selector [ combinator selector | S+ [ combinator? selector ]? ]? ;
    : compound_selector
    | complex_selector combinator compound_selector
    | complex_selector S compound_selector 
    | complex_selector S
        /* for space symbols skipping */
;

compound_selector // : element_name [ HASH | class | attrib | pseudo ]* | [ HASH | class | attrib | pseudo ]+ ;
    : type_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_type_selector", "s", $1);
    }
    | universal_selector type_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_type_selector", "s", $2);
    }
    | universal_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_universal_selector", "", NULL);
    }
    | attribute_selector
    {
        //PyObject_CallMethod((PyObject*)global_self, "handle_universal_selector", "", NULL);
        //PyObject_CallMethod((PyObject*)global_self, "handle_attribute_selector", "", $1);
    }
    | class_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_universal_selector", "", NULL);
        PyObject_CallMethod((PyObject*)global_self, "handle_class_selector", "s", $1);
    }
    | id_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_universal_selector", "", NULL);
        PyObject_CallMethod((PyObject*)global_self, "handle_id_selector", "s", $1);
    }
    | pseudo_class_selector
    {
        //PyObject_CallMethod((PyObject*)global_self, "handle_universal_selector", "", NULL);
        //PyObject_CallMethod((PyObject*)global_self, "handle_pseudo_class_selector", "", $1);
    }
    | compound_selector attribute_selector
    {
        //PyObject_CallMethod((PyObject*)global_self, "handle_attribute_selector", "s", $2);
    }
    | compound_selector class_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_attribute_selector", "s", $2);
    }
    | compound_selector id_selector
    {
        PyObject_CallMethod((PyObject*)global_self, "handle_attribute_selector", "s", $2);
    }
    | compound_selector pseudo_class_selector
    {
        //PyObject_CallMethod((PyObject*)global_self, "handle_attribute_selector", "s", $2);
    }
;

id_selector
    : HASH
    {
        $$ = $1;
    }
;

class_selector // : '.' IDENT ;
    : '.' IDENT
    {
        $$ = $2;
    }
;

type_selector // : IDENT | '*' ;
    : IDENT
    {
        $$ = $1;
    }
;

universal_selector
    : '*'
;

attribute_selector // : '[' S* IDENT S* [ [ '=' | INCLUDES | DASHMATCH ] S* [ IDENT | STRING ] S* ]? ']';
    : '[' spaces IDENT spaces attrib_block ']'
;

attrib_block
    :
    | attrib_block_eq spaces attrib_block_string spaces
;

attrib_block_eq
    : '='
    | INCLUDES
    | DASHMATCH
;

attrib_block_string
    : IDENT
    | STRING
;

pseudo_class_selector // : ':' [ IDENT | FUNCTION S* [IDENT S*]? ')' ] ;
    : ':' pseudo_block
;

pseudo_block
    : IDENT
    | FUNCTION spaces pseudo_block_function_ident ')'
;

pseudo_block_function_ident
    :
    | IDENT spaces
;

declaration // : property ':' S* expr prio? ;
    : property ':' spaces expr prio
    | property ':' spaces expr
;

prio // : IMPORTANT_SYM S* ;
    : IMPORTANT_SYM spaces
;

expr //: term [ operator? term ]*;
    : term
    | expr operator term
    | expr term
;

term // : unary_operator?
     // [ NUMBER S* | PERCENTAGE S* | LENGTH S* | EMS S* | EXS S* | ANGLE S* | TIME S* | FREQ S* ]
     // | STRING S* | IDENT S* | URI S* | hexcolor | function ;
    : unary_operator term_numeral spaces
    | term_numeral spaces
    | STRING spaces
    | IDENT spaces
    | URI spaces
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

function // : FUNCTION S* expr ')' S* ;
    : FUNCTION spaces expr ')' spaces
;


// There is a constraint on the color that it must
// have either 3 or 6 hex-digits (i.e., [0-9a-fA-F])
// after the "#"; e.g., "#000" is OK, but "#abcd" is not.

hexcolor // : HASH S* ;
    : HASH spaces
;

spaces
    :
    | spaces S
;

%%

/* main for manual testing */
main(int argc, char** argv)
{
    const char* usage = "usage: %s [infile [outfile]]\n";
    char* outfile;
    char* infile;
    extern FILE *yyin, *yyout;
    
    char* progname = argv[0];
    
    if(argc > 3)
    {
        fprintf(stderr, usage, progname);
        return 0;
    }
    
    if(argc > 1)
    {
        infile = argv[1];
        yyin = fopen(infile, "r");
        
        if(yyin == NULL)
        {
            fprintf(stderr, "%s: cannot open %s\n", progname, infile);
            return 1;
        }
    }
    
    if(argc > 2)
    {
        infile = argv[2];
        yyout = fopen(outfile, "w");
        
        if(yyout == NULL)
        {
            fprintf(stderr, "%s: cannot open %s\n", progname, outfile);
            return 1;
        }
    }
    
    yyparse();
    
    return 0;
}

yyerror(char *s)
{
    //printf("%s\n", s);
}


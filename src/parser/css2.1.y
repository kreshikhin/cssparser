
%{
%}

%start stylesheet

%token ANGLE
%token BAD_STRING BAD_URI
%token CDC CDO CHARSET_SYM
%token DASHMATCH DIMENSION
%token EMS EXS
%token S STRING
%token FREQ FUNCTION
%token HASH
%token IDENT INCLUDES IMPORT_SYM IMPORTANT_SYM
%token LENGTH
%token MEDIA_SYM
%token NUMBER
%token PAGE_SYM PERCENTAGE 
%token TIME
%token URI

%%

stylesheet // : [ CHARSET_SYM STRING ';' ]?
           //   [S|CDO|CDC]* [ import [ CDO S* | CDC S* ]* ]*
           //   [ [ ruleset | media | page ] [ CDO S* | CDC S* ]* ]* ;
  : charset comments import_block body
;

charset
    :
    | CHARSET_SYM STRING ';'
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
    | ruleset subcomments
    | media subcomments
    | page subcomments
;

subcomments
    :
    | subcomments CDO spaces
    | subcomments CDC spaces
;

import // : IMPORT_SYM S* [STRING|URI] S* media_list? ';' S* ;
    : IMPORT_SYM spaces import_uri spaces media_lists ';' spaces
;

media_lists
    :
    | media_lists media_list
;

import_uri
    : STRING
    | URI
;
    
media // : MEDIA_SYM S* media_list '{' S* ruleset* '}' S* ;
    : MEDIA_SYM spaces media_list '{' spaces rulesets '}' spaces
;

rulesets
    :
    | rulesets ruleset
;

media_list // : medium [ COMMA S* medium]* ;
    : medium media_list_right_part
;

media_list_right_part
    :
    | media_list_right_part ',' spaces medium
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
    | '>' spaces
;

unary_operator // : '-' | '+' ;
    : '-'
    | '+'
;

property // : IDENT S* ;
    : IDENT spaces
;

ruleset // : selector [ ',' S* selector ]* '{' S* declaration? [ ';' S* declaration? ]* '}' S* ;
    : selectors '{' spaces declarations '}' spaces
;

selectors
    : selector
    | selectors ',' spaces selector
;

declarations
    :
    | declaration
    | declarations ';' spaces declaration
    | declarations ';' spaces
;

selector // : simple_selector [ combinator selector | S+ [ combinator? selector ]? ]? ;
    : simple_selector combinator selector
    | simple_selector S spaces combinator selector
    | simple_selector S spaces selector
    | simple_selector S spaces
    | simple_selector
;

simple_selector // : element_name [ HASH | class | attrib | pseudo ]* | [ HASH | class | attrib | pseudo ]+ ;
    : element_name simple_selector_right_part_unreq
    | simple_selector_right_part_req
;

simple_selector_right_part_unreq
    :
    | simple_selector_right_part_req
;

simple_selector_right_part_req
    : simple_selector_right_part
    | simple_selector_right_part_req simple_selector_right_part
;

simple_selector_right_part
    : HASH
    | class
    | attrib
    | pseudo
;

class // : '.' IDENT ;
    : '.' IDENT
;

element_name // : IDENT | '*' ;
    : IDENT
    | '*'
;


attrib // : '[' S* IDENT S* [ [ '=' | INCLUDES | DASHMATCH ] S* [ IDENT | STRING ] S* ]? ']';
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

pseudo // : ':' [ IDENT | FUNCTION S* [IDENT S*]? ')' ] ;
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
    : property ':' spaces expr declaration_prio
;

declaration_prio
    :
    | prio
;

prio // : IMPORTANT_SYM S* ;
    : IMPORTANT_SYM spaces
;

expr //: term [ operator? term ]*;
    : term expr_right_part
;

expr_right_part
    : operator term
    | term
    | expr_right_part operator term
    | expr_right_part term
;

term // : unary_operator?
     // [ NUMBER S* | PERCENTAGE S* | LENGTH S* | EMS S* | EXS S* | ANGLE S* | TIME S* | FREQ S* ]
     // | STRING S* | IDENT S* | URI S* | hexcolor | function ;
    : term_numeral_operator term_numeral spaces
    | STRING spaces | IDENT spaces | URI spaces | hexcolor | function
;

term_numeral_operator
    :
    | unary_operator
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

/*
 * There is a constraint on the color that it must
 * have either 3 or 6 hex-digits (i.e., [0-9a-fA-F])
 * after the "#"; e.g., "#000" is OK, but "#abcd" is not.
 */

hexcolor // : HASH S* ;
    : HASH spaces
;

spaces
    : S
    | spaces S
;

%%



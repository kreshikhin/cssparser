
%{
%}

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

/*
stylesheet
  : [ CHARSET_SYM STRING ';' ]?
    [S|CDO|CDC]* [ import [ CDO S* | CDC S* ]* ]*
    [ [ ruleset | media | page ] [ CDO S* | CDC S* ]* ]*
  ;
import
  : IMPORT_SYM S*
    [STRING|URI] S* media_list? ';' S*
  ;
*/

media
    : MEDIA_SYM spaces media_list '{' spaces rulesets '}' spaces
;

rulesets
    :
    | ruleset
    | ruleset rulesets
;

media_list
    : medium media_list_right_part
;

media_list_right_part
    : ',' spaces medium
;

media_list_right_part_multiple
    :
    | media_list_right_part
    | media_list_right_part_multiple media_list_right_part
;

medium
    : IDENT spaces
;

page
    : PAGE_SYM spaces pseudo_page_unrequired
    '{' spaces declaration_unrequired page_block '}' spaces
;

page_block
    :
    |  ';' spaces declaration_unrequired 
    | page_block  ';' spaces declaration_unrequired 
;

pseudo_page_unrequired
    :
    | pseudo_page
;

pseudo_page
    : ':' IDENT spaces
;

operator
    : '/' spaces
    | ',' spaces
;

combinator
    : '+' spaces
    | '>' spaces
;


unary_operator
    : '-'
    | '+'
    {   print("unary operator\n"); }
;

property
    : IDENT spaces
;

ruleset
    : selector ruleset_selector_block '{' spaces declaration_unrequired ruleset_declaration_block '}' spaces
;

ruleset_selector_block
    :
    | ',' spaces selector
    | ruleset_selector_block ',' spaces selector
;


ruleset_declaration_block
    :
    | ';' spaces declaration_unrequired
    | ruleset_selector_block ';' spaces declaration_unrequired
;

declaration_unrequired
    :
    | declaration
;

selector
    : simple_selector selector_right_part
;



selector_right_part
    :
    | combinator selector
    | selector_spaces 
;

selector_right_part_selector
    :
    | combinator_unrequired selector
;

combinator_unrequired
    :
    | combinator
;

selector_spaces
    : S spaces
;

simple_selector
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

class
    : '.' IDENT
        {   print("class\n");  }
;

element_name
    : IDENT
    | '*'
        {   print("");  }
;


attrib
    : '[' spaces IDENT spaces ']'
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

pseudo
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

declaration
    : property ':' spaces expr declaration_prio
;

declaration_prio
    :
    | prio
;

prio
    : IMPORTANT_SYM spaces
;

expr
    : term
    | term expr_right_part
;

expr_right_part
    : operator term
    | expr_right_part operator term
;

expr_operator
    :
    | operator
;

term
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

function:
    FUNCTION spaces expr ')' spaces
;

/*
 * There is a constraint on the color that it must
 * have either 3 or 6 hex-digits (i.e., [0-9a-fA-F])
 * after the "#"; e.g., "#000" is OK, but "#abcd" is not.
 */

hexcolor
    : HASH spaces
;

spaces
    : S
    | spaces S
;

%%



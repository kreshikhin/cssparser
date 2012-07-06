
%{
#include <stdio.h>
%}

%start stylesheet

%union{
    int integer;
    char* string;
}

%token ANGLE
%token BAD_STRING BAD_URI
%token CDC CDO CHARSET_SYM
%token DASHMATCH DIMENSION
%token EMS EXS
%token S
%token <string> STRING
%token FREQ FUNCTION
%token HASH
%token <string> IDENT
%token INCLUDES IMPORT_SYM IMPORTANT_SYM
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
        {   printf("stylesheet\n");    }
;

charset
    :
        {   printf("empty charset\n");  }
    | CHARSET_SYM STRING ';'
        {   printf("charset : %s\n", $2);    }
;

comments
    :
    | comments S
        {   printf("t\n");  }
    | comments CDO
        {   printf("html open comment combination\n");  }
    | comments CDC
        {   printf("html close comment combination\n"); }
;

import_block
    :
        {   printf("empty imports\n");  }
    | import subcomments
        {   printf("import \n");    }
;

body
    :
        {   printf("empty body\n");  }
    | body ruleset subcomments
        {   printf("body rulesets\n");  }
    | body media subcomments
        {   printf("body media\n");   }
    | body page subcomments
        {   printf("body pagr\n");  }
;

subcomments
    :
    | subcomments CDO spaces
    | subcomments CDC spaces
;

import // : IMPORT_SYM S* [STRING|URI] S* media_list? ';' S* ;
    : IMPORT_SYM spaces import_uri spaces media_lists ';' spaces
        {   printf("import body\n");    }
;

media_lists
    :
        {   printf("empty media lists\n");  }
    | media_lists media_list
        {   printf("media lists\n");  }
;

import_uri
    : STRING
    | URI
;
    
media // : MEDIA_SYM S* media_list '{' S* ruleset* '}' S* ;
    : MEDIA_SYM spaces media_list '{' spaces rulesets '}' spaces
        {   printf("media\n");  }
;

rulesets
    :
        {   printf("empty rulesets\n"); }
    | rulesets ruleset
        {   printf("rulesets\n");   }
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
    | '>' spaces
;

unary_operator // : '-' | '+' ;
    : '-'
    | '+'
;

property // : IDENT S* ;
    : IDENT spaces
        {   printf("property\n");   }
;

ruleset // : selector [ ',' S* selector ]* '{' S* declaration? [ ';' S* declaration? ]* '}' S* ;
    : selectors '{' spaces declarations '}' spaces
        {   printf("ruleset\n");    }
;

selectors
    : selector
        {   printf("selectors1\n");    }
    | selectors ',' spaces selector
        {   printf("selectors2\n");    }
;

declarations
    :
        {   printf("empty declarations\n");  }
    | declaration
        {   printf("declarations1\n");   }
    | declarations ';' spaces declaration
        {   printf("declarations2\n");   }
    | declarations ';' spaces
        {   printf("declarations3\n");   }
;

selector // : simple_selector [ combinator selector | S+ [ combinator? selector ]? ]? ;
    : simple_selector combinator selector
        {   printf("selector1\n");    }
    | simple_selector S spaces combinator selector
        {   printf("selector2\n");    }
    | simple_selector S spaces selector
        {   printf("selector3\n");    }
    | simple_selector S spaces
        {   printf("selector4\n");    }
    | simple_selector
        {   printf("selector5\n");    }
;

simple_selector // : element_name [ HASH | class | attrib | pseudo ]* | [ HASH | class | attrib | pseudo ]+ ;
    : element_name
        {   printf("simple selector2\n");    }
    | selector_prefix
        {   printf("simple selector with right part\n");    }
    | simple_selector selector_prefix
        {   printf("simple selector with right part without element name\n");    }
;

selector_prefix
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
        {   printf("ident :%s\n", $1);  }
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
    : property ':' spaces expr prio
    {   printf("declaration1\n");   }
    | property ':' spaces expr
    {   printf("declaration2\n");   }
;

prio // : IMPORTANT_SYM S* ;
    : IMPORTANT_SYM spaces
;

expr //: term [ operator? term ]*;
    : term
    {   printf("expr1\n");   }
    | expr operator term
    {   printf("expr2\n");   }
    | expr term
    {   printf("exp3\n");   }
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
    {   printf("empty space\n");   }
    | spaces S
    {   printf("many spaces\n");    }
;

%%

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
    printf("%s\n", s);
}


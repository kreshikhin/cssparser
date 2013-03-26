%{
#include "y.tab.h"
#include "cssparser.h"

#define RETURN_TEXT(token) \
    do { \
        yylval.string = css_arena_copy(yytext, (size_t)yyleng); \
        if (!yylval.string) yylval.string = (char*)""; \
        return (token); \
    } while (0)

#define YY_USER_ACTION \
    do { \
        yylloc.first_line = css_line; \
        yylloc.first_column = css_column; \
        css_advance_pos(&css_line, &css_column, yytext, (size_t)yyleng); \
        yylloc.last_line = css_line; \
        yylloc.last_column = css_column; \
    } while (0);
%}

%option case-insensitive
%option noyywrap
%option nounput
%option noinput
%option never-interactive

h              [0-9a-f]
nonascii       [\240-\377]
unicode        \\{h}{1,6}(\r\n|[ \t\r\n\f])?
escape         {unicode}|\\[^\r\n\f0-9a-f]
nmstart        [_a-z]|{nonascii}|{escape}
nmchar         [_a-z0-9-]|{nonascii}|{escape}
string1        \"([^\n\r\f\\"]|\\{nl}|{escape})*\"
string2        \'([^\n\r\f\\']|\\{nl}|{escape})*\'
badstring1     \"([^\n\r\f\\"]|\\{nl}|{escape})*\\?
badstring2     \'([^\n\r\f\\']|\\{nl}|{escape})*\\?
badcomment1    \/\*[^*]*\*+([^/*][^*]*\*+)*
badcomment2    \/\*[^*]*(\*+[^/*][^*]*)*
baduri1        url\({w}((?-i:[!#$%&*-\[\]-~])|{nonascii}|{escape})*{w}
baduri2        url\({w}{string}{w}
baduri3        url\({w}{badstring}
comment        \/\*[^*]*\*+([^/*][^*]*\*+)*\/
ident          -?{nmstart}{nmchar}*
name           {nmchar}+
num            [0-9]+|[0-9]*"."[0-9]+
string         {string1}|{string2}
badstring      {badstring1}|{badstring2}
badcomment     {badcomment1}|{badcomment2}
baduri         {baduri1}|{baduri2}|{baduri3}
url            ([!#$%&*-~]|{nonascii}|{escape})*
s              [ \t\r\n\f]+
w              {s}?
nl             \n|\r\n|\r|\f

A              a|\\0{0,4}(41|61)(\r\n|[ \t\r\n\f])?
C              c|\\0{0,4}(43|63)(\r\n|[ \t\r\n\f])?
D              d|\\0{0,4}(44|64)(\r\n|[ \t\r\n\f])?
E              e|\\0{0,4}(45|65)(\r\n|[ \t\r\n\f])?
G              g|\\0{0,4}(47|67)(\r\n|[ \t\r\n\f])?|\\g
H              h|\\0{0,4}(48|68)(\r\n|[ \t\r\n\f])?|\\h
I              i|\\0{0,4}(49|69)(\r\n|[ \t\r\n\f])?|\\i
K              k|\\0{0,4}(4b|6b)(\r\n|[ \t\r\n\f])?|\\k
L              l|\\0{0,4}(4c|6c)(\r\n|[ \t\r\n\f])?|\\l
M              m|\\0{0,4}(4d|6d)(\r\n|[ \t\r\n\f])?|\\m
N              n|\\0{0,4}(4e|6e)(\r\n|[ \t\r\n\f])?|\\n
O              o|\\0{0,4}(4f|6f)(\r\n|[ \t\r\n\f])?|\\o
P              p|\\0{0,4}(50|70)(\r\n|[ \t\r\n\f])?|\\p
R              r|\\0{0,4}(52|72)(\r\n|[ \t\r\n\f])?|\\r
S              s|\\0{0,4}(53|73)(\r\n|[ \t\r\n\f])?|\\s
T              t|\\0{0,4}(54|74)(\r\n|[ \t\r\n\f])?|\\t
U              u|\\0{0,4}(55|75)(\r\n|[ \t\r\n\f])?|\\u
X              x|\\0{0,4}(58|78)(\r\n|[ \t\r\n\f])?|\\x
Z              z|\\0{0,4}(5a|7a)(\r\n|[ \t\r\n\f])?|\\z

%%

{s}                     { return S; }

\/\*[^*]*\*+([^/*][^*]*\*+)*\/       /* ignore comments */
{badcomment}                         /* unclosed comment at EOF */

"<!--"                  /* CDO, ignored between rules */
"-->"                   /* CDC, ignored between rules */

"~="                    { RETURN_TEXT(INCLUDES); }
"|="                    { RETURN_TEXT(DASHMATCH); }

{string}                { RETURN_TEXT(STRING); }
{badstring}             { return BAD_STRING; }

{ident}                 { RETURN_TEXT(IDENT); }

"#"{name}               { RETURN_TEXT(HASH); }

@{I}{M}{P}{O}{R}{T}     { return IMPORT_SYM; }
@{P}{A}{G}{E}           { return PAGE_SYM; }
@{M}{E}{D}{I}{A}        { return MEDIA_SYM; }
"@charset "             { return CHARSET_SYM; }

"!"({w}|{comment})*{I}{M}{P}{O}{R}{T}{A}{N}{T}  { return IMPORTANT_SYM; }

{num}{E}{M}             { RETURN_TEXT(EMS); }
{num}{E}{X}             { RETURN_TEXT(EXS); }
{num}{P}{X}             { RETURN_TEXT(LENGTH); }
{num}{C}{M}             { RETURN_TEXT(LENGTH); }
{num}{M}{M}             { RETURN_TEXT(LENGTH); }
{num}{I}{N}             { RETURN_TEXT(LENGTH); }
{num}{P}{T}             { RETURN_TEXT(LENGTH); }
{num}{P}{C}             { RETURN_TEXT(LENGTH); }
{num}{D}{E}{G}          { RETURN_TEXT(ANGLE); }
{num}{R}{A}{D}          { RETURN_TEXT(ANGLE); }
{num}{G}{R}{A}{D}       { RETURN_TEXT(ANGLE); }
{num}{M}{S}             { RETURN_TEXT(TIME); }
{num}{S}                { RETURN_TEXT(TIME); }
{num}{H}{Z}             { RETURN_TEXT(FREQ); }
{num}{K}{H}{Z}          { RETURN_TEXT(FREQ); }
{num}{ident}            { RETURN_TEXT(DIMENSION); }
{num}%                  { RETURN_TEXT(PERCENTAGE); }
{num}                   { RETURN_TEXT(NUMBER); }

"url("{w}{string}{w}")" { RETURN_TEXT(URI); }
"url("{w}{url}{w}")"    { RETURN_TEXT(URI); }
{baduri}                { return BAD_URI; }

{ident}"("              { RETURN_TEXT(FUNCTION); }

.                       { return (unsigned char)*yytext; }

%%

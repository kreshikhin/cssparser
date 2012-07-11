#!/bin/bash

flex -d css2.1.l
yacc -d css2.1.y
gcc -c lex.yy.c y.tab.c
gcc -o parser lex.yy.o y.tab.o -lfl

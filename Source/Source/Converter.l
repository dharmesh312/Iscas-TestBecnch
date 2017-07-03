%{
#include <stdio.h>

#include "Gate.hxx"
#include "NetPort.hxx"
#include "Converter.hxx"

/* Stores the line number */
/*"INPUT"  { return INPUT ; } */
/*[\n]   { g_lineNo++ ; }*/
/*STRING [^{FIRSTCHARAT}#()=, \t\n]*/
extern int g_lineNo ;
%}

FIRSTCHARAT {^_}
WHITESPACE [ \t\n]
ALLWH {WHITESPACE}
STRING [^#()=, \t\n]

%x COMMENT 
%%
"INPUT"  { return INPUT ; } 
"OUTPUT" { return OUTPUT ; }
"AND"    { return AND ; }
"OR"     { return OR ; }
"BUFF"    { return BUFF ; }
"NOT"    { return NOT ; }
"XOR"    { return XOR ; }
"NOR"    { return NOR ; }    
"XNOR"   { return XNOR ; }
"NAND"   { return NAND ; }
"="      { return '=' ; }
","      { return ',' ; }
"("      { return '(' ; }
")"      { return ')' ; }
[ \t]  {;/* Eat up the white spaces*/ }
[\n]   { g_lineNo++ ; }
"#"    { BEGIN(COMMENT) ; }
{STRING}* { 
             if(yytext[0] == '_') 
             { 
                 return ILL_IDENTIFIER; 
             } 
             yylval.sname = strdup(yytext) ; 
             return IDENTIFIER ; 
          }
<COMMENT>[\n] { g_lineNo ++ ; BEGIN(INITIAL) ; }
<COMMENT>.    { ; }

%%

%{

/* System Includes */
#include <cstdio>
#include <vector>

/* Project Includes */
#include "Gate.hxx"
#include "NetPort.hxx"
#include "Design.hxx"
#include "Application.hxx"

/* Parser related declarations */
extern int yylex();
extern int yyerror(const char* msg) ;
extern FILE* yyin ;
int g_lineNo ;
char* g_fileName ;
int g_errCount ;


%}

%union {
    char* sname ;
    iscus2verilog::eDirection edirection ;
    iscus2verilog::eGateType egate ;
    std::vector<char*>* snamelist ;
}


%token INPUT
%token OUTPUT
%token AND
%token OR
%token BUFF
%token NOT
%token XOR
%token NOR
%token XNOR
%token NAND

%token<sname> IDENTIFIER
%token ILL_IDENTIFIER

%type<egate> gatedecl
%type<edirection> netportdecl
%type<snamelist> identifierlist

%start source 

%%

source : linelist 
       | error 
       ;

linelist : line linelist
         | /* blank to consume empty file */
         ;

line : netportdecl '(' IDENTIFIER ')'
       {
           /* First check whether the net/port is 
            * already declared or not, if it is not 
            * declared the create one 
            */
            if(NULL == iscus2verilog::Application::getDesign()->getNetPort($3)) {
                iscus2verilog::NetPort* np =  new iscus2verilog::NetPort($3,$1) ;
                iscus2verilog::Application::getDesign()->addNetPort(np) ;

                // If this is input type then the boolean 
                // expression attached to this is the name 
                // itself .
                if($1 == iscus2verilog::NETPORT_DIR_INPUT) {
                    np->setBooleanExpression($3) ;    
                }
            } else {
                /* Redeclaration error. */
            }
           
       }
     | IDENTIFIER '=' gatedecl '(' identifierlist ')'
       {
           /* First check whether the output identifier is declared or not */
           iscus2verilog::NetPort* outputPort = iscus2verilog::Application::getDesign()->getNetPort($1) ;
           if(NULL == outputPort) {
               /* That means we need to create this net */
               outputPort = new iscus2verilog::NetPort($1) ;
               iscus2verilog::Application::getDesign()->addNetPort(outputPort) ;
           } else { 
               /* Do a sanity check, and produce a warning.
                  At the output side only a output port or 
                  a wire can appear, if anything else appear 
                  then thats a warning case.
                */
               if(iscus2verilog::NETPORT_DIR_UNSET != outputPort->getDirection() 
                  && iscus2verilog::NETPORT_DIR_OUTPUT != outputPort->getDirection()) {
                   printf("[WARN 1003] Direction mismatch for port/net %s\n",outputPort->getName()) ;
               }
           }
           
           /* Now create the gate with the output port */
           iscus2verilog::Gate* gate = new iscus2verilog::Gate($3) ;
           gate->addOutput(outputPort) ;

           /* Now traverse over the input port list.
            * If any of them can not be found on the 
            * design symbol table, then create them 
            * as nets(i.e with no direction 
            */
           std::vector<char*>::iterator netportlist = $5->begin() ;
           std::string* gateExpression = NULL ;
           bool firstNet = true ;
           while(netportlist != $5->end()) {
               char* name = *netportlist ;
               iscus2verilog::NetPort* netport = iscus2verilog::Application::getDesign()->getNetPort(name) ;
               if(NULL == netport) {
                   netport = new iscus2verilog::NetPort(name) ;
                   iscus2verilog::Application::getDesign()->addNetPort(netport) ;
               } else {
                   if(iscus2verilog::NETPORT_DIR_UNSET != netport->getDirection() 
                      && iscus2verilog::NETPORT_DIR_INPUT != netport->getDirection()) {
                       printf("[WARN 1004] Direction mismatch for port/net %s\n", netport->getName()) ;
                   }
               }
  
               netportlist++ ;
                   
               gate->addInput(netport) ;
               if(true == firstNet) {
                   gateExpression = new std::string("(") ;
                   firstNet = false ;
               } else {
                   char* gateType = iscus2verilog::Application::getLibraryModuleName($3) ;
                   (*gateExpression) += " " ;
                   (*gateExpression) += gateType ;
                   (*gateExpression) += " (" ;
               }
               char* netExpression = (char*)netport->getBooleanExpr() ;
               if(netExpression) {
                   (*gateExpression) += netExpression;
               } else { 
                   // Give a warning of float net 
               }
               (*gateExpression) += ")" ;
           }
           outputPort->setBooleanExpression((char*)gateExpression->c_str()) ;

           /* Finally add this gate to the design */
           iscus2verilog::Application::getDesign()->addGate(gate) ;
       }
     ;

identifierlist : IDENTIFIER { $$ = new std::vector<char*>() ; $$->push_back($1) ; }
               | IDENTIFIER ',' identifierlist { $3->push_back($1) ; $$ = $3 ; }
               ;

netportdecl : INPUT { $$ = iscus2verilog::NETPORT_DIR_INPUT ; }
            | OUTPUT { $$ = iscus2verilog::NETPORT_DIR_OUTPUT ; }
            ;

gatedecl : AND { $$ = iscus2verilog::ISCUS_GATE_AND ; }
         | OR { $$ = iscus2verilog::ISCUS_GATE_OR ; }
         | BUFF { $$ = iscus2verilog::ISCUS_GATE_BUFF ; }
         | NOT { $$ = iscus2verilog::ISCUS_GATE_NOT ; }
         | XOR { $$ = iscus2verilog::ISCUS_GATE_XOR ; }
         | NOR { $$ = iscus2verilog::ISCUS_GATE_NOR ; }
         | XNOR { $$ = iscus2verilog::ISCUS_GATE_XNOR ; }
         | NAND { $$ = iscus2verilog::ISCUS_GATE_NAND ; }
         ;
%%



int parseIscus(char* filename)
{
    yyin = fopen(filename,"r") ;
    g_fileName = filename ;
    g_lineNo = 1 ;
    g_errCount = 0 ;
    yyparse() ;    
    return g_errCount > 0 ? 1 : 0 ;
}

int yyerror(const char* msg) {
    printf("\n[ERROR 1005] Parse error at FILE : %s, LINE : %d\n",g_fileName, g_lineNo) ;
    g_errCount ++ ;
    return 0 ;
}

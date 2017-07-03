/* System Includes */
#include <cstdio>
#include <cstring>

/* Project Includes */
#include "Design.hxx"
#include "Application.hxx"
#include "Gate.hxx"
#include "NetPort.hxx"

/* External declaration for parser function */
extern int parseIscus(char*) ;
extern int g_errCount ;

iscus2verilog::Design* iscus2verilog::Application::_design = NULL ;

namespace iscus2verilog {
    
    Design* Application::getDesign() { 
        return _design ;
    }

    char* Application::getLibraryModuleName(eGateType egatetype) {
        switch(egatetype) {
            case ISCUS_GATE_AND : return strdup("and") ;
            case ISCUS_GATE_OR : return strdup("or") ;
            case ISCUS_GATE_BUFF : return strdup("buff") ;
            case ISCUS_GATE_NOT : return strdup("not") ;
            case ISCUS_GATE_XOR : return strdup("xor") ;
            case ISCUS_GATE_NOR : return strdup("nor") ;
            case ISCUS_GATE_XNOR : return strdup("xnor") ;
            case ISCUS_GATE_NAND : return strdup("nand") ;
            default : return NULL ;
        }
    }

    Application::Application(int argc,char** argv) {
        if(argc < 3 ) {
            /* Print usage */
        }
        _inpFilename = argv[1] ;
        char* topModuleName = argv[2] ;
        _outpFileName = argv[3] ;

        _design = new Design(topModuleName) ;
    }

    eStatus Application::parse() {
        if(!parseIscus(_inpFilename)) {
            printf("\n[INFO 1000] Succeessfully parsed %s\n",_inpFilename) ;
            return PARSE_SUCCESSFUL ;
        } else {
            printf("\n[ERROR 1001] %d Error(s) in parsing file %s\n",g_errCount,_inpFilename) ;
            return PARSE_UNSUCCESSFUL ;
        }
        
    }

    void Application::decompile() {
        FILE* outFilePtr = fopen(_outpFileName,"w") ;
        Design* design = _design ;
        fprintf(outFilePtr, "module %s(", _design->getName()) ;
        
        std::map<std::string, NetPort*> netportlist = _design->getNetPortList() ;
        std::vector<NetPort*> outputPortList ;
        std::vector<NetPort*> inputPortList ;
        std::vector<NetPort*> wireList ;
        std::map<std::string, NetPort*>::iterator itr = netportlist.begin();
        bool firstport = true ;
        while(itr != netportlist.end()) {
            NetPort* np = (*itr).second ;
            if(NETPORT_DIR_UNSET == np->getDirection()) {
                wireList.push_back(np) ;
            } else {

                if(true == firstport) {
                    fprintf(outFilePtr," %s",np->getName()) ;
                    firstport = false ;
                } else {
                    fprintf(outFilePtr,", %s",np->getName()) ;
                }

                if(NETPORT_DIR_INPUT == np->getDirection()) {
                    inputPortList.push_back(np) ;
                } else {
                    outputPortList.push_back(np) ;
                }
            }
            itr++ ;
        }
        fprintf(outFilePtr,");\n") ;

        fprintf(outFilePtr,"\n") ;


        std::vector<NetPort*>::iterator it = outputPortList.begin() ;
        fprintf(outFilePtr,"\toutput ") ;
        firstport = true ;
        while(it != outputPortList.end()) {
            if(true == firstport) {
                fprintf(outFilePtr," %s", (*it)->getName()) ;
                firstport = false ;
            } else {
                fprintf(outFilePtr,", %s",(*it)->getName()) ;
            }
            it++ ;
        }
        fprintf(outFilePtr,";\n");

        it = inputPortList.begin() ;
        fprintf(outFilePtr,"\tinput ") ;
        firstport = true ;
        while(it != inputPortList.end()) {
            if(true == firstport) {
                fprintf(outFilePtr," %s",(*it)->getName() ) ;
                firstport = false ;
            } else {
                fprintf(outFilePtr,", %s",(*it)->getName()) ;
            }
            it++ ;    
        }
        fprintf(outFilePtr,";\n") ;

        it = wireList.begin() ;
        fprintf(outFilePtr,"\twire ") ;
        firstport = true;
        while(it != wireList.end()) {
            if(true == firstport) {
                fprintf(outFilePtr," %s",(*it)->getName()) ;
                firstport = false ;
            } else {
                fprintf(outFilePtr,", %s",(*it)->getName()) ;
            }
            it++ ;
        }
        fprintf(outFilePtr,";\n") ;

        fprintf(outFilePtr,"\n") ;
        fprintf(outFilePtr,"\n") ;

        std::vector<Gate*> gatelist = _design->getGateList() ;
        std::vector<Gate*>::iterator gateIter = gatelist.begin() ;
        int instancecount = 0 ;
        while(gateIter != gatelist.end()) {
            Gate* gt = (*gateIter) ;
            fprintf(outFilePtr,"\t%s ",Application::getLibraryModuleName(gt->getMasterType())) ;
            fprintf(outFilePtr,"instance_%d(%s",instancecount,const_cast<NetPort*>(gt->getOutput())->getName()) ;
            instancecount ++ ;
            std::vector<NetPort*> inputlist = gt->getInputList() ;
            std::vector<NetPort*>::iterator inputiter = inputlist.begin() ;
            while(inputiter != inputlist.end()) {
                fprintf(outFilePtr,", %s",(*inputiter)->getName()) ;
                inputiter ++ ;
            }
            fprintf(outFilePtr," );\n") ;
            gateIter ++ ;
        }
            
        fprintf(outFilePtr,"\n") ;
        fprintf(outFilePtr,"\n") ;

        fprintf(outFilePtr,"endmodule\n") ;
    }

    void Application::printLogic() {
        Design* design = _design ;
        std::map<std::string, NetPort*> netportlist = _design->getNetPortList() ;
		std::map<std::string, NetPort*>::iterator itr = netportlist.begin();
        while(itr != netportlist.end()) {
            NetPort* np = (*itr).second ;
            if(NETPORT_DIR_OUTPUT == np->getDirection()) {
                char* booleanExpr = (char*)np->getBooleanExpr() ;
                printf("\n[INFO 1010] Boolean expression associated with output port %s : %s\n",np->getName() , booleanExpr) ;
            }
            itr++ ;
        }
    }
}

int main(int argc, char** argv) {

    /* Create the application and compile the iscus file */
    iscus2verilog::Application* thisApp = new iscus2verilog::Application(argc,argv) ;

    /* Parse the iscus file and populate the object model */
    iscus2verilog::eStatus parseStatus = thisApp->parse() ;
    if(iscus2verilog::PARSE_SUCCESSFUL == parseStatus) {
        /* If parsing was successful , then 
         * decompile the object model into a 
         * verilog file 
         */
        thisApp->decompile() ;
    thisApp->printLogic() ;
    }
    return 0 ;
}

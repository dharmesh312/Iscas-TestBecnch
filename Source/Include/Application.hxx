#ifndef __APPLICATION_HXX_
#define __APPLICATION_HXX_

#include "Gate.hxx"

namespace iscus2verilog {
    class Design ;
    typedef enum Status {
        PARSE_SUCCESSFUL = 0 ,
        PARSE_UNSUCCESSFUL
    } eStatus ;
    class Application {
        private :
            static Design* _design;
            char* _outpFileName ;
            char* _inpFilename ;

        public :
            static char*  getLibraryModuleName(eGateType gatetype) ;
            Application(int argc,char** argv) ;
            ~Application() {;}

            static Design* getDesign() ;

            void decompile() ;
			void printLogic() ;
            eStatus parse() ;
    };
}
#endif

#ifndef __DESIGN_HXX_
#define __DESIGN_HXX_

#include <string>
#include <map>
#include <vector>

namespace iscus2verilog {
    /* Forward declaration of used classes */
    class NetPort ;
    class Gate ;
    /*! Class to represent the entire design */
    class Design {
        private :
            std::string _name ; //!< Represents the design name.
            std::map<std::string , NetPort*> _netPortList ; //!< Represents all the net port list
            //std::vector<NetPort*> _netList ; //!< Represents the netlist 
            //std::vector<NetPort*> _portList ; //!< Represents the port list 
            std::vector<Gate*> _gateList; //!< Represents the gate list in the design 
            
        public :
            Design(std::string name){
                _name = name ;
            }

            ~Design() {}

            const char* getName() { return _name.c_str(); }

            void addNetPort(NetPort* );
            void addGate(Gate* ) ;
            
            NetPort* getNetPort(std::string );

            //const std::vector<NetPort*>& getNetList() ;
			//const std::vector<NetPort*>& getPortList() ;

            const std::map<std::string, NetPort*>& getNetPortList() ;
            const std::vector<Gate*>& getGateList();
    };
}

#endif

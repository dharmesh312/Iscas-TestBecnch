#ifndef __GATE_HXX_
#define __GATE_HXX_

#include <string>
#include <vector>

namespace iscus2verilog {

    class NetPort ;
    typedef enum GateType {
        ISCUS_GATE_UNSET = -1 , 
        ISCUS_GATE_AND =0 ,
        ISCUS_GATE_OR,
        ISCUS_GATE_BUFF,
        ISCUS_GATE_NOT,
        ISCUS_GATE_XOR,
        ISCUS_GATE_NOR,
        ISCUS_GATE_XNOR,
        ISCUS_GATE_NAND
    } eGateType ;

    /*! Class to represent the gate instance */
    class Gate {
        private :
            eGateType _masterType ; //!< Represents the name of the master.
            NetPort* _output ; //!< Holds the output port.
            std::vector<NetPort*> _inputList ; //!< Holds the input list.
        
        public : 
            Gate(eGateType type) {
                _masterType = type ;
            }

            ~Gate() {} 

            void addOutput(NetPort* ) ;
            void addInput(NetPort* ) ;

            const eGateType getMasterType() ;
            const NetPort* getOutput() ;
            const std::vector<NetPort*>& getInputList() ;
    };
}
#endif

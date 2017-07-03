#include "Gate.hxx"

namespace iscus2verilog {
    void Gate::addOutput(NetPort* netPort) {
        _output = netPort ;
    }
    
    void Gate::addInput(NetPort* netPort) {
        _inputList.push_back(netPort) ;
    }

    const eGateType Gate::getMasterType() {
        return _masterType ;
    }
    
    const NetPort* Gate::getOutput() {
        return _output ;
    }
    
    const std::vector<NetPort*>& Gate::getInputList() {
        return _inputList ;
    }
}

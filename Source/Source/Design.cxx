
/* Project Includes */
#include "Design.hxx"
#include "NetPort.hxx"
#include "Gate.hxx"

namespace iscus2verilog {

    void Design::addNetPort(NetPort* netPort) {
        _netPortList[netPort->getName()] = netPort ;
        /*
        if(NETPORT_DIR_UNSET == netport->getDirection()) {
            _netList.push_back(netPort);
        }
        else {
            _portList.push_back(netPort) ;
        } */
        return ;
    }

    void Design::addGate(Gate* gate) {
        _gateList.push_back(gate) ;
        return ;
    }

    NetPort* Design::getNetPort(std::string name) {
        
        if(_netPortList.count(name) > 0) {
            return _netPortList[name] ;
        }

        return NULL ;
    }

    const std::map<std::string, NetPort*>& Design::getNetPortList() {
        return _netPortList ;
    }

    const std::vector<Gate*>& Design::getGateList() {
        return _gateList ;
    }
}

#ifndef __NET_PORT_HXX_
#define __NET_PORT_HXX_

#include <string>

namespace iscus2verilog {
    /*! Enum to represent the direction */
    typedef enum Direction {
        NETPORT_DIR_UNSET = -1 , 
        NETPORT_DIR_INPUT = 0 ,  //!< Represents the input direction.
        NETPORT_DIR_OUTPUT,      //!< Represents the output direction.
        NETPORT_DIR_INOUT        //!< Represents the inout direction. 
    } eDirection ;

    typedef enum NetPortType {
       NETPORT_TYPE_UNSET = -1 ,
       NETPORT_TYPE_NET = 0 ,
       NETPORT_TYPE_PORT = 1 
    } eNetPortType ;

    /*! Class to represent input and output pins 
         *  written in iscus format. While converting 
         *  them to verilog we will decompile them as 
         *  net and port of proper direction.
         */
    class NetPort {
        private :
            std::string _name ; //!< Represents the name.
            eDirection  _direction ; //!< Represents the direction.    
            std::string *_booleanExpr ; 
            /*eNetPortType _type ; */
        public :
            NetPort(std::string name, eDirection direction = NETPORT_DIR_UNSET) {
                _name = name ;
                _direction = direction ;
                _booleanExpr = NULL ;
            }

            ~NetPort() {}
        
            eDirection getDirection() { return _direction ; }
            void setDirection(eDirection dir) { _direction = dir ; }

            const char* getName() { return _name.c_str() ; }

            void setBooleanExpression(char* expression) { _booleanExpr = new std::string(expression) ;  }
            const char* getBooleanExpr() { return _booleanExpr->c_str() ; }
        
            //eNetPortType getType() { return _type ; }
    } ;
}
#endif

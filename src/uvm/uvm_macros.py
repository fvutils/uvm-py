'''
Created on Oct 7, 2019

@author: ballance
'''
from uvm.base.component_registry import uvm_component_registry

def uvm_component_utils(T):
    '''
    Registers a UVM Component with the type system
    '''
    
    def uvm_component_get_type():
        pass

    T.type_id = uvm_component_registry(T)
    
    return T 

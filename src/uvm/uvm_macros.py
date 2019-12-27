'''
Created on Oct 7, 2019

@author: ballance
'''
from uvm.base.component_registry import uvm_component_registry
from uvm.base.object_registry import uvm_object_registry

def uvm_component_utils(T):
    '''
    Registers a UVM Component with the type system
    '''
    
    def uvm_component_get_type():
        pass

    T.type_id = uvm_component_registry(T)
    
    return T 

def uvm_object_utils(T):
    
    T.type_id = uvm_object_registry(T)
    
    return T

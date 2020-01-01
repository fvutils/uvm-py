'''
Created on Oct 7, 2019

@author: ballance
'''
from uvm.base.component_registry import uvm_component_registry
from uvm.base.object_registry import uvm_object_registry
from uvm.base.object_wrapper import uvm_object_wrapper
from uvm.base.globals import uvm_report_enabled, uvm_report_info,\
    uvm_report_fatal, uvm_report_error, uvm_report_warning
from uvm.base.object_globals import UVM_INFO, UVM_WARNING, UVM_NONE, UVM_FATAL,\
    UVM_ERROR

def uvm_component_utils(T):
    '''
    Registers a UVM Component with the type system
    '''
    
    def uvm_component_get_type():
        pass
    
    def uvm_component_get_object_type():
        pass

    T.type_id = uvm_component_registry(T)
    T.get_type = uvm_component_get_type
    T.get_object_type = uvm_component_get_object_type
    
    from uvm.base.coreservice import uvm_coreservice_t
    cs = uvm_coreservice_t.get()
    cs.get_factory().register(uvm_object_wrapper(T))
    
    return T 

def uvm_object_utils(T):
    
    def uvm_object_get_type():
        pass
    
    def uvm_object_get_object_type():
        pass
    
    T.type_id = uvm_object_registry(T)
    T.get_type = uvm_object_get_type
    T.get_object_type = uvm_object_get_object_type
    # TODO: virtual create() method
    
    return T

def uvm_fatal(id, msg):
    if uvm_report_enabled(UVM_NONE, UVM_FATAL, id):
        # TODO: find calling context using inspect
        file = "<unknown>"
        line = -1
        uvm_report_fatal(id, msg, UVM_NONE, file, line, "", True)
        
def uvm_error(id, msg):
    if uvm_report_enabled(UVM_NONE, UVM_ERROR, id):
        # TODO: find calling context using inspect
        file = "<unknown>"
        line = -1
        uvm_report_error(id, msg, UVM_NONE, file, line, "", True)
        
def uvm_warning(id, msg):
    if uvm_report_enabled(UVM_NONE, UVM_WARNING, id):
        # TODO: find calling context using inspect
        file = "<unknown>"
        line = -1
        uvm_report_warning(id, msg, UVM_NONE, file, line, "", True)
        
    
def uvm_info(name, msg, verbosity):
    if uvm_report_enabled(verbosity, UVM_INFO, id):
        # TODO: find calling context using inspect
        file = "<unknown>"
        line = -1
        uvm_report_info(id, msg, verbosity, file, line, "", True)


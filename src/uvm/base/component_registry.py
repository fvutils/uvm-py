'''
Created on Oct 8, 2019

@author: ballance
'''

class uvm_component_registry():
    
    def __init__(self, cls):
        self.target_cls = cls
        
    def create(self, name, parent):
        return self.target_cls(name, parent)
    
'''
Created on Oct 8, 2019

@author: ballance
'''

class uvm_object_registry():
    
    def __init__(self, cls):
        self.target_cls = cls
        
    def create(self, name = ""):
        if name == "":
            return self.target_cls()
        else:
            return self.target_cls(name)

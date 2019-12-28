'''
Created on Dec 27, 2019

@author: ballance
'''
import cocotb
import cocotb.triggers
from cocotb import scheduler

try:
    import unittest
    from unittest.case import TestCase
    import uvm
    from uvm.uvm_macros import uvm_component_utils, uvm_object_utils
    from uvm.base.component import uvm_component
    from uvm.base.globals import run_test
    from uvm.base.object import uvm_object
except:
    print("Execption: ")
    
class my_sim():
    
    def __init__(self):
        pass
    
    def register_timed_callback(self, sim_steps, callback, hndl):
        print("register_timed_callback")
        
    def deregister_callback(self, hndl):
        print("deregister_callback")
    
    

class TestSmoke(TestCase):
    
    def setUp(self):
        global simulator
        cocotb.triggers.simulator = my_sim()
        
    def test_smoke(self):
        print("test_smoke")
        
        @uvm_component_utils
        class my_component(uvm_component):
            
            def __init__(self, name, parent):
                super().__init__(name, parent)

        print("--> add_test")        
        scheduler.add_test(run_test("my_component"))
        print("<-- add_test")        
        
#        yield [task.join()]
        
    def test_create(self):
        
        @uvm_object_utils
        class my_object(uvm_object):
            
            def __init__(self, name="my_object"):
                super().__init__(name)
                
        o = my_object.type_id.create("abc")
        print("o=" + str(type(o)))
        o2 = o.create("def")
        print("o2=" + str(type(o2)))

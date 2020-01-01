'''
Created on Dec 27, 2019

@author: ballance
'''
import cocotb
import cocotb.triggers
from cocotb import scheduler
from cocotb.scheduler import _debug
import logging
import sys
from cocotb.simulator_base import SimulatorBase
from cocotb.info import Info

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
    
class my_sim(SimulatorBase):
    
    def __init__(self):
        super().__init__()
    
class TestSmoke(TestCase):
    
    def setUp(self):
        global simulator
        global _debug
   #     global cocotb.argv
  
        info = Info()
   
        self.core = cocotb.initialize_context(info, my_sim())

        h = logging.StreamHandler(sys.stdout)
        logger = logging.getLogger()
        logger.addHandler(h)
        h.flush()
        
    def test_smoke(self):
        print("test_smoke")
        
        @uvm_component_utils
        class my_component(uvm_component):
            
            def __init__(self, name, parent):
                super().__init__(name, parent)
                print("my_component::init")

        print("--> add_test")        
        task = scheduler.add_test(run_test("my_component"))
        print("<-- add_test")        


        print("--> yield task: " + str(task))
#        yield task.join()
        print("<-- yield task")        
        
    def test_create(self):
        
        @uvm_object_utils
        class my_object(uvm_object):
            
            def __init__(self, name="my_object"):
                super().__init__(name)
                
        o = my_object.type_id.create("abc")
        print("o=" + str(type(o)))
        o2 = o.create("def")
        print("o2=" + str(type(o2)))

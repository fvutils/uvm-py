'''
Created on Dec 29, 2019

@author: ballance
'''
import cocotb

class Mailbox():
    
    def __init__(self):
        self.data = []
        self.data_avail_ev = cocotb.triggers.Event()
    
    def try_put(self, data):
        self.data.append(data)
        self.data_avail_ev.set()
        return True
   
    @cocotb.coroutine 
    def get(self):
        while len(self.data) == 0:
            yield self.data_avail_ev.wait()

        return self.data.pop(0)
        
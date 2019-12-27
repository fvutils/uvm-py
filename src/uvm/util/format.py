'''
Created on Dec 25, 2019

@author: ballance
'''

def sformatf(fmt, *args):
    print("TODO: formatf fmt=" + fmt)
    return strcat(fmt, *args)

def strcat(*args):
    ret = ""
    
    for a in args:
        ret += a
        
    return ret

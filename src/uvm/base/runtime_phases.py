#
#----------------------------------------------------------------------
# Copyright 2007-2011 Mentor Graphics Corporation
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2011 AMD
# Copyright 2014-2018 NVIDIA Corporation
# Copyright 2013 Cisco Systems, Inc.
# Copyright 2019 Matthew Ballance
#   All Rights Reserved Worldwide
#
#   Licensed under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in
#   compliance with the License.  You may obtain a copy of
#   the License at
#
#       http:#www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in
#   writing, software distributed under the License is
#   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.  See
#   the License for the specific language governing
#   permissions and limitations under the License.
#----------------------------------------------------------------------
from uvm.base.task_phase import uvm_task_phase
import cocotb

# Title -- NODOCS -- UVM Run-Time Phases
# 
# The run-time schedule is the pre-defined phase schedule
# which runs concurrently to the <uvm_run_phase> global run phase.
# By default, all <uvm_component>s using the run-time schedule
# are synchronized with respect to the pre-defined phases in the schedule.
# It is possible for components to belong to different domains
# in which case their schedules can be unsynchronized.
#
# The names of the UVM phases (which will be returned by get_name() for a
# phase instance) match the class names specified below with the "uvm_"
# and "_phase" removed.  For example, the main phase corresponds to the 
# uvm_main_phase class below and has the name "main", which means that 
# the following can be used to call foo() at the start of main phase:
#
# | function void phase_started(uvm_phase phase) ;
# |    if (phase.get_name()=="main") foo() ;
# | endfunction
# 
# The run-time phases are executed in the sequence they are specified below.
# 
# 


# @uvm-ieee 1800.2-2017 auto 9.8.2.1
class uvm_pre_reset_phase (uvm_task_phase):
    
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.pre_reset_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_pre_reset_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_pre_reset_phase.m_inst is None):
            uvm_pre_reset_phase.m_inst = uvm_pre_reset_phase()
        return uvm_pre_reset_phase.m_inst

    def __init__(self, name="pre_reset"):
        super().__init__(name)

# @uvm-ieee 1800.2-2017 auto 9.8.2.2
class uvm_reset_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.reset_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_reset_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_reset_phase.m_inst is None):
            uvm_reset_phase.m_inst = uvm_reset_phase()
        return uvm_reset_phase.m_inst

    def __init__(self, name="reset"):
        super().__init__(name)


# @uvm-ieee 1800.2-2017 auto 9.8.2.3
class uvm_post_reset_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.post_reset_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_post_reset_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_post_reset_phase.m_inst is None):
            uvm_post_reset_phase.m_inst = uvm_post_reset_phase()
        return uvm_post_reset_phase.m_inst

    def __init__(self, name="post_reset"):
        super().__init__(name)

# @uvm-ieee 1800.2-2017 auto 9.8.2.4
class uvm_pre_configure_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.pre_configure_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_pre_configure_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_pre_configure_phase.m_inst is None):
            uvm_pre_configure_phase.m_inst = uvm_pre_configure_phase()
        return uvm_pre_configure_phase.m_inst

    def __init__(self, name="pre_configure"):
        super().__init__(name)

# @uvm-ieee 1800.2-2017 auto 9.8.2.5
class uvm_configure_phase(uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.configure_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_configure_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_configure_phase.m_inst is None):
            uvm_configure_phase.m_inst = uvm_configure_phase()
        return uvm_configure_phase.m_inst

    def __init__(self, name="configure"):
        super().__init__(name); 


# @uvm-ieee 1800.2-2017 auto 9.8.2.6
class uvm_post_configure_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.post_configure_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_post_configure_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_post_configure_phase.m_inst is None):
            uvm_post_configure_phase.m_inst = uvm_post_configure_phase()
        return uvm_post_configure_phase.m_inst

    def __init__(self, name="post_configure"):
        super().__init__(name); 

# @uvm-ieee 1800.2-2017 auto 9.8.2.7
class uvm_pre_main_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.pre_main_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_pre_main_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_pre_main_phase.m_inst is None):
            uvm_pre_main_phase.m_inst = uvm_pre_main_phase()
        return uvm_pre_main_phase.m_inst

    def __init__(self, name="pre_main"):
        super().__init__(name)


# @uvm-ieee 1800.2-2017 auto 9.8.2.8
class uvm_main_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.main_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_main_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_main_phase.m_inst is None):
            uvm_main_phase.m_inst = uvm_main_phase()
        return uvm_main_phase.m_inst

    def __init__(self, name="main"):
        super().__init__(name)

# @uvm-ieee 1800.2-2017 auto 9.8.2.9
class uvm_post_main_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.post_main_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_post_main_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_post_main_phase.m_inst is None):
            uvm_post_main_phase.m_inst = uvm_post_main_phase()
        return uvm_post_main_phase.m_inst

    def __init__(self, name="post_main"):
        super().__init__(name)

# @uvm-ieee 1800.2-2017 auto 9.8.2.10
class uvm_pre_shutdown_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.pre_shutdown_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_pre_shutdown_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_pre_shutdown_phase.m_inst is None):
            uvm_pre_shutdown_phase.m_inst = uvm_pre_shutdown_phase()
        return uvm_pre_shutdown_phase.m_inst

    def __init__(self, name="pre_shutdown"):
        super().__init__(name)

# @uvm-ieee 1800.2-2017 auto 9.8.2.11
class uvm_shutdown_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.shutdown_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_shutdown_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_shutdown_phase.m_inst is None):
            uvm_shutdown_phase.m_inst = uvm_shutdown_phase()
        return uvm_shutdown_phase.m_inst

    def __init__(self, name="shutdown"):
        super().__init__(name)


# @uvm-ieee 1800.2-2017 auto 9.8.2.12
class uvm_post_shutdown_phase (uvm_task_phase):
    @cocotb.coroutine
    def exec_task(self, comp, phase):
        yield comp.post_shutdown_phase(phase)

    m_inst = None
#   `uvm_type_name_decl("uvm_post_shutdown_phase")

    # Function -- NODOCS -- get
    # Returns the singleton phase handle 
    @staticmethod
    def get():
        if (uvm_post_shutdown_phase.m_inst is None):
            uvm_post_shutdown_phase.m_inst = uvm_post_shutdown_phase()
        return uvm_post_shutdown_phase.m_inst
    
    def __init__(self, name="post_shutdown"):
        super().__init__(name)
        

#
#----------------------------------------------------------------------
# Copyright 2007-2014 Mentor Graphics Corporation
# Copyright 2014 Semifore
# Copyright 2010-2014 Synopsys, Inc.
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2011-2012 AMD
# Copyright 2013-2018 NVIDIA Corporation
# Copyright 2012-2017 Cisco Systems, Inc.
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
from uvm.base.object import uvm_object
from uvm.uvm_macros import uvm_object_utils

#------------------------------------------------------------------------------
#
# Class -- NODOCS -- uvm_phase_state_change
#
#------------------------------------------------------------------------------
#
# Phase state transition descriptor.
# Used to describe the phase transition that caused a
# <uvm_phase_cb::phase_state_changed()> callback to be invoked.
#

# @uvm-ieee 1800.2-2017 auto 9.3.2.1
@uvm_object_utils
class uvm_phase_state_change (uvm_object):

    def __init__(self, name="uvm_phase_state_change"):
        super().__init__(name)
        
        self.m_phase = None
        self.m_prev_state = None
        self.m_jump_to = None

    # @uvm-ieee 1800.2-2017 auto 9.3.2.2.1
    def get_state(self):
        return self.m_phase.get_state()

    # @uvm-ieee 1800.2-2017 auto 9.3.2.2.2
    def get_prev_state(self):
        return self.m_prev_state

    # @uvm-ieee 1800.2-2017 auto 9.3.2.2.3
    def jump_to(self):
        return self.m_jump_to
    
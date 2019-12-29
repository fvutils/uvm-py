#
#----------------------------------------------------------------------
# Copyright 2007-2011 Mentor Graphics Corporation
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2011 AMD
# Copyright 2015 NVIDIA Corporation
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
from uvm.base.phase import uvm_phase
from uvm.base.object_globals import uvm_phase_type, uvm_phase_state

#------------------------------------------------------------------------------
#
# Class -- NODOCS -- uvm_topdown_phase
#
#------------------------------------------------------------------------------
# Virtual base class for function phases that operate top-down.
# The pure virtual function execute() is called for each component.
#
# A top-down function phase completes when the <execute()> method
# has been called and returned on all applicable components
# in the hierarchy.

# @uvm-ieee 1800.2-2017 auto 9.7.1
class uvm_topdown_phase(uvm_phase):


    # @uvm-ieee 1800.2-2017 auto 9.7.2.1
    def __init__(self, name):
        super().__init__(name,uvm_phase_type.UVM_PHASE_IMP)



    # @uvm-ieee 1800.2-2017 auto 9.7.2.2
    def traverse(self, comp, phase, state):
        from uvm.base.domain import uvm_domain
        
#        string name;
        phase_domain = phase.get_domain()
        comp_domain = comp.get_domain()

        if self.m_phase_trace:
            print("TODO: `uvm_info")
#    `uvm_info("PH_TRACE",$sformatf("topdown-phase phase=%s state=%s comp=%s comp.domain=%s phase.domain=%s",
#          phase.get_name(), state.name(), comp.get_full_name(),comp_domain.get_name(),phase_domain.get_name()),
#          UVM_DEBUG)

        if phase_domain == uvm_domain.get_common_domain() or phase_domain == comp_domain:
            if state == uvm_phase_state.UVM_PHASE_STARTED:
                comp.m_current_phase = phase
                comp.m_apply_verbosity_settings(phase)
                comp.phase_started(phase)
            elif state == uvm_phase_state.UVM_PHASE_EXECUTING:
                if phase.get_name() != "build" or not comp.m_build_done:
                    ph = self
                    comp.m_phasing_active += 1
                    if self in comp.m_phase_imps.keys():
                        ph = comp.m_phase_imps[self]
                    ph.execute(comp, phase)
                    comp.m_phasing_active -= 1
            elif state == uvm_phase_state.UVM_PHASE_READY_TO_END:
                comp.phase_ready_to_end(phase)
            elif state == uvm_phase_state.UVM_PHASE_ENDED:
                comp.phase_ended(phase)
                comp.m_current_phase = None
            else:
                print("TODO: `uvm_fatal")
#            `uvm_fatal("PH_BADEXEC","topdown phase traverse internal error")
        for cn in comp.m_children.keys():
            self.traverse(comp.m_children[cn], phase, state)


    # @uvm-ieee 1800.2-2017 auto 9.7.2.3
    def execute(self, comp, phase):
        # reseed this process for random stability
        print("TODO: reseed from thread")
#        process proc = process::self();
#        proc.srandom(uvm_create_random_seed(phase.get_type_name(), comp.get_full_name()));

        comp.m_current_phase = phase
        self.exec_func(comp,phase)


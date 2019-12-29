#
#----------------------------------------------------------------------
# Copyright 2007-2011 Mentor Graphics Corporation
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2011 AMD
# Copyright 2013-2015 NVIDIA Corporation
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
from uvm.base.object_globals import uvm_phase_type, uvm_phase_state
from uvm.base.phase import uvm_phase
import cocotb

#------------------------------------------------------------------------------
#
# Class -- NODOCS -- uvm_task_phase
#
#------------------------------------------------------------------------------
# Base class for all task phases.
# It forks a call to <uvm_phase::exec_task()>
# for each component in the hierarchy.
#
# The completion of the task does not imply, nor is it required for, 
# the end of phase. Once the phase completes, any remaining forked 
# <uvm_phase::exec_task()> threads are forcibly and immediately killed.
#
# By default, the way for a task phase to extend over time is if there is
# at least one component that raises an objection.  
#| class my_comp (uvm_component):;
#|    task main_phase(uvm_phase phase);
#|       phase.raise_objection(this, "Applying stimulus")
#|       ...
#|       phase.drop_objection(this, "Applied enough stimulus")
#|    endtask
#| endclass
# 
#   
# There is however one scenario wherein time advances within a task-based phase
# without any objections to the phase being raised. If two (or more) phases 
# share a common successor, such as the <uvm_run_phase> and the 
# <uvm_post_shutdown_phase> sharing the <uvm_extract_phase> as a successor, 
# then phase advancement is delayed until all predecessors of the common 
# successor are ready to proceed.  Because of this, it is possible for time to 
# advance between <uvm_component::phase_started> and <uvm_component::phase_ended>
# of a task phase without any participants in the phase raising an objection.
#

# @uvm-ieee 1800.2-2017 auto 9.6.1
class uvm_task_phase (uvm_phase):

    # @uvm-ieee 1800.2-2017 auto 9.6.2.1
    def __init__(self, name):
        super().__init__(name,uvm_phase_type.UVM_PHASE_IMP)

    # @uvm-ieee 1800.2-2017 auto 9.6.2.2
    def traverse(self, comp, phase, state):
        phase.m_num_procs_not_yet_returned = 0
        self.m_traverse(comp, phase, state)

    def m_traverse(self, comp, phase, state):
        from uvm.base.domain import uvm_domain
        phase_domain = phase.get_domain()
        comp_domain = comp.get_domain()
        seqr = None

        for cn in comp.m_children.keys():
            self.m_traverse(comp.m_children[cn], phase, state)    
    
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
    
                print("TODO: check if component is a sequencer")
    #            if ($cast(seqr, comp))
    #                seqr.start_phase_sequence(phase);
            elif state == uvm_phase_state.UVM_PHASE_EXECUTING:
                ph = self
                if self in comp.m_phase_imps.keys():
                    ph = comp.m_phase_imps[self]
                ph.execute(comp, phase)
            elif state == uvm_phase_state.UVM_PHASE_READY_TO_END: 
                comp.phase_ready_to_end(phase)
            elif state == uvm_phase_state.UVM_PHASE_ENDED: 
                print("TODO: check if component is a sequencer")
    #          if ($cast(seqr, comp))
    #            seqr.stop_phase_sequence(phase);
                comp.phase_ended(phase)
                comp.m_current_phase = None
            else:
                print("TODO: uvm_fatal")
    #          `uvm_fatal("PH_BADEXEC","task phase traverse internal error")

    @cocotb.coroutine
    def forked_task(self, comp, phase):
        # reseed this process for random stability
        # TODO: reseed
#        proc = process::self();
#        proc.srandom(uvm_create_random_seed(phase.get_type_name(), comp.get_full_name()));

        phase.m_num_procs_not_yet_returned += 1

        yield self.exec_task(comp,phase)

        phase.m_num_procs_not_yet_returned -= 1


    # @uvm-ieee 1800.2-2017 auto 9.6.2.3
    def execute(self, comp, phase):
        cocotb.fork(self.forked_task(comp, phase))


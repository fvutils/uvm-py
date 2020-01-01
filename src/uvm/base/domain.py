#
#----------------------------------------------------------------------
# Copyright 2007-2018 Mentor Graphics Corporation
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2011 AMD
# Copyright 2015-2018 NVIDIA Corporation
# Copyright 2012 Accellera Systems Initiative
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
from uvm.base.phase import uvm_phase
from uvm.base.object_globals import uvm_phase_type
from uvm.base.common_phases import uvm_build_phase, uvm_connect_phase,\
    uvm_end_of_elaboration_phase, uvm_start_of_simulation_phase, uvm_run_phase,\
    uvm_extract_phase, uvm_check_phase, uvm_report_phase, uvm_final_phase
from uvm.base.runtime_phases import uvm_pre_reset_phase, uvm_reset_phase,\
    uvm_post_reset_phase, uvm_pre_configure_phase, uvm_configure_phase,\
    uvm_post_configure_phase, uvm_pre_main_phase, uvm_main_phase,\
    uvm_post_main_phase, uvm_pre_shutdown_phase, uvm_shutdown_phase,\
    uvm_post_shutdown_phase
from uvm.uvm_macros import uvm_error
from uvm.util.format import sformatf

# uvm_phase build_ph;
# uvm_phase connect_ph;
# uvm_phase end_of_elaboration_ph;
# uvm_phase start_of_simulation_ph;
# uvm_phase run_ph;
# uvm_phase extract_ph;
# uvm_phase check_ph;
# uvm_phase report_ph;
   
#------------------------------------------------------------------------------
#
# Class -- NODOCS -- uvm_domain
#
#------------------------------------------------------------------------------
#
# Phasing schedule node representing an independent branch of the schedule.
# Handle used to assign domains to components or hierarchies in the testbench
#

# @uvm-ieee 1800.2-2017 auto 9.4.1
class uvm_domain (uvm_phase):

    m_uvm_domain = None # run-time phases
    m_domains = {} # map<string,uvm_domain>
    m_uvm_schedule = None

    # @uvm-ieee 1800.2-2017 auto 9.4.2.2
    @staticmethod
    def get_domains(domains):
        domains.clear()
        domains.extend(uvm_domain.m_domains)


    # Function -- NODOCS -- get_uvm_schedule
    #
    # Get the "UVM" schedule, which consists of the run-time phases that
    # all components execute when participating in the "UVM" domain.
    #
    @staticmethod
    def get_uvm_schedule():
        uvm_domain.get_uvm_domain()
        return uvm_domain.m_uvm_schedule

    # Function -- NODOCS -- get_common_domain
    #
    # Get the "common" domain, which consists of the common phases that
    # all components execute in sync with each other. Phases in the "common"
    # domain are build, connect, end_of_elaboration, start_of_simulation, run,
    # extract, check, report, and final.
    #
    @staticmethod
    def get_common_domain():
        domain = None

        if "common" in uvm_domain.m_domains.keys():
            domain = uvm_domain.m_domains["common"]
    
        if domain is not None:
            return domain

        domain = uvm_domain("common")
        domain.add(uvm_build_phase.get())
        domain.add(uvm_connect_phase.get())
        domain.add(uvm_end_of_elaboration_phase.get())
        domain.add(uvm_start_of_simulation_phase.get())
        domain.add(uvm_run_phase.get())
        domain.add(uvm_extract_phase.get())
        domain.add(uvm_check_phase.get())
        domain.add(uvm_report_phase.get())
        domain.add(uvm_final_phase.get())

        # for backward compatibility, make common phases visible;
        # same as uvm_<name>_phase::get().
        print("TODO: back-compat -- retrieve phases")
#         build_ph               = domain.find(uvm_build_phase::get());
#         connect_ph             = domain.find(uvm_connect_phase::get());
#         end_of_elaboration_ph  = domain.find(uvm_end_of_elaboration_phase::get());
#         start_of_simulation_ph = domain.find(uvm_start_of_simulation_phase::get());
#         run_ph                 = domain.find(uvm_run_phase::get());   
#         extract_ph             = domain.find(uvm_extract_phase::get());
#         check_ph               = domain.find(uvm_check_phase::get());
#         report_ph              = domain.find(uvm_report_phase::get());
# 
#         domain = uvm_domain.get_uvm_domain()
#         uvm_domain.m_domains["common"].add(
#             domain,
#             with_phase=uvm_domain.m_domains["common"].find(uvm_run_phase::get()))


        return uvm_domain.m_domains["common"]


    # @uvm-ieee 1800.2-2017 auto 9.4.2.3
    @staticmethod
    def add_uvm_phases(schedule):
        schedule.add(uvm_pre_reset_phase.get())
        schedule.add(uvm_reset_phase.get())
        schedule.add(uvm_post_reset_phase.get())
        schedule.add(uvm_pre_configure_phase.get())
        schedule.add(uvm_configure_phase.get())
        schedule.add(uvm_post_configure_phase.get())
        schedule.add(uvm_pre_main_phase.get())
        schedule.add(uvm_main_phase.get())
        schedule.add(uvm_post_main_phase.get())
        schedule.add(uvm_pre_shutdown_phase.get())
        schedule.add(uvm_shutdown_phase.get())
        schedule.add(uvm_post_shutdown_phase.get())


    # Function -- NODOCS -- get_uvm_domain
    #
    # Get a handle to the singleton ~uvm~ domain
    #
    @staticmethod
    def get_uvm_domain():
        if uvm_domain.m_uvm_domain is None:
            uvm_domain.m_uvm_domain = uvm_domain("uvm")
            uvm_domain.m_uvm_schedule = uvm_phase("uvm_sched", uvm_phase_type.UVM_PHASE_SCHEDULE)
            uvm_domain.add_uvm_phases(uvm_domain.m_uvm_schedule)
            uvm_domain.m_uvm_domain.add(uvm_domain.m_uvm_schedule)
            
        return uvm_domain.m_uvm_domain

    # @uvm-ieee 1800.2-2017 auto 9.4.2.1
    def __init__(self, name):
        super().__init__(name,uvm_phase_type.UVM_PHASE_DOMAIN)
        if name in uvm_domain.m_domains.keys():
            uvm_error("UNIQDOMNAM", sformatf("Domain created with non-unique name '%s'", name))
        uvm_domain.m_domains[name] = self

    # @uvm-ieee 1800.2-2017 auto 9.4.2.4
    def jump(self, phase):
        print("TODO: uvm_domain.jump")
#         phases = []
#         
#         m_get_transitive_children(phases);
#     
#         phases = phases.find(item) with (item.get_state() inside {[UVM_PHASE_STARTED:UVM_PHASE_CLEANUP]}); 
#     
#         for ph in phases:
#             if ph.is_before(phase) or ph.is_after(phase):
#                 ph.jump(phase)

# jump_all
# --------
    @staticmethod
    def jump_all(phase):
        domains = {}
        
        uvm_domain.get_domains(domains)
           
        for domain in domains:
            domain.jump(phase)

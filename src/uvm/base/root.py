#
#------------------------------------------------------------------------------
# Copyright 2007-2011 Mentor Graphics Corporation
# Copyright 2014 Semifore
# Copyright 2010-2018 Synopsys, Inc.
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2010-2012 AMD
# Copyright 2012-2018 NVIDIA Corporation
# Copyright 2012-2018 Cisco Systems, Inc.
# Copyright 2012 Accellera Systems Initiative
# Copyright 2017 Verific
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
#------------------------------------------------------------------------------
from uvm.base.component import uvm_component
from uvm.base.object_globals import m_uvm_core_state, uvm_core_state, UVM_NONE
import cocotb
from uvm.base.factory import uvm_factory
from cocotb.utils import get_sim_time
from uvm.base.coreservice import uvm_coreservice_t
from cocotb.result import TestComplete
from cocotb.triggers import Timer
from uvm.util.format import sformatf
from cocotb import fork


#------------------------------------------------------------------------------
#
# CLASS -- NODOCS -- uvm_root
#
# The ~uvm_root~ class serves as the implicit top-level and phase controller for
# all UVM components. Users do not directly instantiate ~uvm_root~. The UVM
# automatically creates a single instance of <uvm_root> that users can
# access via the global (uvm_pkg-scope) variable, ~uvm_top~.
#
# (see uvm_ref_root.gif)
#
# The ~uvm_top~ instance of ~uvm_root~ plays several key roles in the UVM.
#
# Implicit top-level - The ~uvm_top~ serves as an implicit top-level component.
# Any component whose parent is specified as ~null~ becomes a child of ~uvm_top~.
# Thus, all UVM components in simulation are descendants of ~uvm_top~.
#
# Phase control - ~uvm_top~ manages the phasing for all components.
#
# Search - Use ~uvm_top~ to search for components based on their
# hierarchical name. See <find> and <find_all>.
#
# Report configuration - Use ~uvm_top~ to globally configure
# report verbosity, log files, and actions. For example,
# ~uvm_top.set_report_verbosity_level_hier(UVM_FULL)~ would set
# full verbosity for all components in simulation.
#
# Global reporter - Because ~uvm_top~ is globally accessible (in uvm_pkg
# scope), UVM's reporting mechanism is accessible from anywhere
# outside ~uvm_component~, such as in modules and sequences.
# See <uvm_report_error>, <uvm_report_warning>, and other global
# methods.
#
#
# The ~uvm_top~ instance checks during the end_of_elaboration phase if any errors have
# been generated so far. If errors are found a UVM_FATAL error is being generated as result
# so that the simulation will not continue to the start_of_simulation_phase.
#

#------------------------------------------------------------------------------

# Class: uvm_root
# 
#| class uvm_root (uvm_component):
#
# Implementation of the uvm_root class, as defined
# in 1800.2-2017 Section F.7

#@uvm-ieee 1800.2-2017 manual F.7
class uvm_root(uvm_component):

    m_uvm_timeout_overridable = True
    
    # Variable- phase_timeout
    #
    # Specifies the timeout for the run phase. Default is `UVM_DEFAULT_TIMEOUT
    # TODO: determine actual timeout
#    time phase_timeout = `UVM_DEFAULT_TIMEOUT;
    phase_timeout = 0

    # Function -- NODOCS -- get()
    # Static accessor for <uvm_root>.
    #
    # The static accessor is provided as a convenience wrapper
    # around retrieving the root via the <uvm_coreservice_t::get_root>
    # method.
    #
    # | # Using the uvm_coreservice_t:
    # | uvm_coreservice_t cs;
    # | uvm_root r;
    # | cs = uvm_coreservice_t::get();
    # | r = cs.get_root();
    # |
    # | # Not using the uvm_coreservice_t:
    # | uvm_root r;
    # | r = uvm_root::get();
    #
    @staticmethod
    def get():
        cs = uvm_coreservice_t.get()
        return cs.get_root()

    def get_type_name(self):
        return "uvm_root"


    #----------------------------------------------------------------------------
    # Group -- NODOCS -- Simulation Control
    #----------------------------------------------------------------------------


    # Task -- NODOCS -- run_test
    #
    # Phases all components through all registered phases. If the optional
    # test_name argument is provided, or if a command-line plusarg,
    # +UVM_TESTNAME=TEST_NAME, is found, then the specified component is created
    # just prior to phasing. The test may contain new verification components or
    # the entire testbench, in which case the test and testbench can be chosen from
    # the command line without forcing recompilation. If the global (package)
    # variable, finish_on_completion, is set, then $finish is called after
    # phasing completes.

    @cocotb.coroutine
    def run_test(self, test_name=""):
        global m_uvm_core_state

        test_names = []

        uvm_run_test_callback.m_do_pre_run_test()

        factory = uvm_factory.get()
        m_uvm_core_state = uvm_core_state.PRE_RUN

        testname_plusarg = False

        # Set up the process that decouples the thread that drops objections from
        # the process that processes drop/all_dropped objections. Thus, if the
        # original calling thread (the "dropper") gets killed, it does not affect
        # drain-time and propagation of the drop up the hierarchy.
        # Needs to be done in run_test since it needs to be in an
        # initial block to fork a process.
        uvm_objection.m_init_objections()

        # dump cmdline args BEFORE the args are being used
        self.m_do_dump_args()

        # Retrieve the test names provided on the command line.  Command line
        # overrides the argument.
        test_name_count = self.clp.get_arg_values("+UVM_TESTNAME=", test_names)

        # If at least one, use first in queue.
        if test_name_count > 0:
            test_name = test_names[0]
            testname_plusarg = True

        # If multiple, provided the warning giving the number, which one will be
        # used and the complete list.
        if test_name_count > 1:
            test_list = ""
            for i in range(len(test_names)):
                if i != 0:
                    test_list += ", "
                test_list += test_names[i]
            self.uvm_report_warning("MULTTST",
                sformatf("Multiple (%0d) +UVM_TESTNAME arguments provided on the command line.  '%s' will be used.  Provided list: %s.", test_name_count, test_name, test_list), UVM_NONE)

        # if test now defined, create it using common factory
        if test_name != "":
            if "uvm_test_top" in self.m_children.keys():
                self.uvm_report_fatal("TTINST",
                    "An uvm_test_top already exists via a previous call to run_test", UVM_NONE)
#                #0; # forces shutdown because $finish is forked
                yield Timer(0)
            
        uvm_test_top = factory.create_component_by_name(test_name, "", "uvm_test_top", None)

        if uvm_test_top is None:
            if testname_plusargs:
                msg = "command line +UVM_TESTNAME=" + test_name
            else:
                msg = "call to run_test(" + test_name + ")"
            self.uvm_report_fatal("INVTST",
                "Requested test from "+msg+ " not found.", UVM_NONE);

        if len(self.m_children) == 0:
            uvm_report_fatal("NOCOMP",
                "No components instantiated. You must either instantiate"+
                    " at least one component before calling run_test or use"+
                    " run_test to do so. To run a test using run_test,"+
                    " use +UVM_TESTNAME or supply the test name in"+
                    " the argument to run_test(). Exiting simulation.", UVM_NONE)
            return

        if test_name=="":
            self.uvm_report_info("RNTST", "Running test ...", UVM_LOW)
        elif test_name == uvm_test_top.get_type_name():
            self.uvm_report_info("RNTST", "Running test "+test_name+"...", UVM_LOW);
        else:
            self.uvm_report_info("RNTST", "Running test "+uvm_test_top.get_type_name()+" (via factory override for test \""+test_name+"\")...", UVM_LOW);

    # store thread forked below for final cleanup
    # phase runner, isolated from calling process
    phase_runner_proc = fork(uvm_phase.m_run_phases())
    
    #0; # let the phase runner start
    yield Timer(0)

    # TODO:
    wait (m_phase_all_done == 1);

    m_uvm_core_state=UVM_CORE_POST_RUN;

    # clean up after ourselves
    phase_runner_proc.kill()

    l_rs = uvm_report_server.get_server();

    uvm_run_test_callback.m_do_post_run_test();

    l_rs.report_summarize();

    m_uvm_core_state = UVM_CORE_FINISHED
    
    if self.get_finish_on_completion():
        raise TestComplete()

    # Function -- NODOCS -- die
    #
    # This method is called by the report server if a report reaches the maximum
    # quit count or has a UVM_EXIT action associated with it, e.g., as with
    # fatal errors.
    #
    # Calls the <uvm_component::pre_abort()> method
    # on the entire <uvm_component> hierarchy in a bottom-up fashion.
    # It then calls <uvm_report_server::report_summarize> and terminates the simulation
    # with ~$finish~.

    def die(self):
        global m_uvm_core_state
        
        l_rs = uvm_report_server.get_server()
        # do the pre_abort callbacks

        m_uvm_core_state = uvm_core_state.PRE_ABORT

        self.m_do_pre_abort()

        uvm_run_test_callback.m_do_pre_abort()

        l_rs.report_summarize()

        m_uvm_core_state = uvm_core_state.ABORTED

        # TODO: handle abort
#        $finish;

    # Function -- NODOCS -- set_timeout
    #
    # Specifies the timeout for the simulation. Default is <`UVM_DEFAULT_TIMEOUT>
    #
    # The timeout is simply the maximum absolute simulation time allowed before a
    # ~FATAL~ occurs.  If the timeout is set to 20ns, then the simulation must end
    # before 20ns, or a ~FATAL~ timeout will occur.
    #
    # This is provided so that the user can prevent the simulation from potentially
    # consuming too many resources (Disk, Memory, CPU, etc) when the testbench is
    # essentially hung.
    #
    #

    
    def set_timeout(self, timeout, overridable=True):
        if not uvm_root.m_uvm_timeout_overridable:
            # TODO: Error handling
#            uvm_report_info("NOTIMOUTOVR",
#                    $sformatf("The global timeout setting of %0d is not overridable to %0d due to a previous setting.",
#                    phase_timeout, timeout), UVM_NONE);
            return
        self.m_uvm_timeout_overridable = overridable;
        self.phase_timeout = timeout;        
        

    # Variable -- NODOCS -- finish_on_completion
    #
    # If set, then run_test will call $finish after all phases are executed.

    # Function -- NODOCS -- get_finish_on_completion
  
    def get_finish_on_completion(self):
        return self.finish_on_completion

    # Function -- NODOCS -- set_finish_on_completion

    def set_finish_on_completion(self, f):
        self.finish_on_completion = f
   
#----------------------------------------------------------------------------
# Group -- NODOCS -- Topology
#----------------------------------------------------------------------------

    # Function -- NODOCS -- find

    def find(self, comp_match):
        comp_list = []

        self.find_all(comp_match,comp_list)

        if len(comp_list) > 1:
            # TODO: Error handling
#             self.uvm_report_warning("MMATCH",
#                 $sformatf("Found %0d components matching '%s'. Returning first match, %0s.",
#                 comp_list.size(),comp_match,comp_list[0].get_full_name()), UVM_NONE)
            pass

        if len(comp_list) == 0:
            self.uvm_report_warning("CMPNFD",
                "Component matching '"+comp_match+
                "' was not found in the list of uvm_components", UVM_NONE)
            return None

        return comp_list[0]

    # Function -- NODOCS -- find_all
    #
    # Returns the component handle (find) or list of components handles
    # (find_all) matching a given string. The string may contain the wildcards,
    # * and ?. Strings beginning with '.' are absolute path names. If the optional
    # argument comp is provided, then search begins from that component down
    # (default=all components).

    def find_all(self, comp_match, comps, comp=None):
        if comp is None:
            comp = self
            
        self.m_find_all_recurse(comp_match, comps, comp)



    # Function -- NODOCS -- print_topology
    #
    # Print the verification environment's component topology. The
    # ~printer~ is a <uvm_printer> object that controls the format
    # of the topology printout; a ~null~ printer prints with the
    # default output.

    def print_topology(self, printer=None):
        if len(m_children) == 0:
            self.uvm_report_warning("EMTCOMP", 
                "print_topology - No UVM components to print.", UVM_NONE)
            return

        if printer is None:
            printer = uvm_printer.get_default()

        # TODO: Info printing
        # `uvm_info("UVMTOP","UVM testbench topology:",UVM_NONE)
        self.print(printer)


    # Function: set_enable_print_topology
    #
    #| function void set_enable_print_topology (bit enable)
    #
    # Sets the variable to enable printing the entire testbench topology just after completion
    # of the end_of_elaboration phase.
        #
        # @uvm-accellera The details of this API are specific to the Accellera implementation, and are not being considered for contribution to 1800.2

    def set_enable_print_topology(self, enable):
        self.enable_print_topology = enable
        
    # Function: get_enable_print_topology
    #
    #| function bit get_enable_print_topology()
    #
    # Gets the variable to enable printing the entire testbench topology just after completion.
        #
        # @uvm-accellera The details of this API are specific to the Accellera implementation, and are not being considered for contribution to 1800.2

    def get_enable_print_topology(self):
        return self.enable_print_topology


    # PRIVATE members
    def m_find_all_recurse(self, comp_match, comps, comp=None):
        # TODO: seems a non-Pythonic way of doing things
        name = ""

        if comp.get_first_child(name):
           while True: 
               self.m_find_all_recurse(comp_match, comps, comp.get_child(name))
               
               if not comp.get_next_child(name):
                   break
               
        if self.uvm_is_match(comp_match, comp.get_full_name()) and comp.get_name() != "": # uvm_top
            comps.append(comp)

    def __init__ (self):
        super().__init__("__top__", None)
        
        # For error reporting purposes, we need to construct this first.
        rh = uvm_report_handler("reporter");
        self.set_report_handler(rh);

        # Checking/Setting this here makes it much harder to
        # trick uvm_init into infinite recursions
        if uvm_root.m_inst is not None:
            # TODO: Error handling
#            `uvm_fatal_context("UVM/ROOT/MULTI",
#                       "Attempting to construct multiple roots",
#                       m_inst)
            return
        uvm_root.m_inst = self

        self.clp = uvm_cmdline_processor.get_inst()
        self.finish_on_completion = True
        
		# Variable -- NODOCS -- enable_print_topology
		#
		# If set, then the entire testbench topology is printed just after completion
		# of the end_of_elaboration phase.
        self.enable_print_topology = False
        
        self.m_phase_all_done = False;
          
    def m_add_child (self, child):
        if super().m_add_child(child):
            return True
        else:
            return False
        
    def build_phase(self, phase):
        super().build_phase(phase)
        
        self.m_set_cl_msg_args()

        self.m_do_verbosity_settings()
        self.m_do_timeout_settings()
        self.m_do_factory_settings()
        self.m_do_config_settings()
        self.m_do_max_quit_settings()
       
        # TODO: 
#     extern local function void m_do_verbosity_settings();
#     extern local function void m_do_timeout_settings();
#     extern local function void m_do_factory_settings();
#     extern local function void m_process_inst_override(string ovr);
#     extern local function void m_process_type_override(string ovr);
#     extern local function void m_do_config_settings();
#     extern local function void m_do_max_quit_settings();
    
    def m_do_dump_args(self):
        dump_args = []
        all_args = []
        out_string = ""
        
        if self.clp.get_arg_matches("+UVM_DUMP_CMDLINE_ARGS", dump_args):
            clp.get_args(all_args)
            for i,arg in enumerate(all_args):
                self.uvm_report_info("DUMPARGS", sformatf("idx=%0d arg=[%s]",idx,all_args[idx]), UVM_NONE)

    # TODO:
#     extern local function void m_process_config(string cfg, bit is_int);
#     extern local function void m_process_default_sequence(string cfg);
#     extern function void m_check_verbosity();
#     extern function void m_check_uvm_field_flag_size();
#     extern virtual function void report_header(UVM_FILE file = 0);
    
    # singleton handle
    m_inst = None

    # For error checking
    @cocotb.coroutine
    def run_phase(self, uvm_phase phase):
        # check that the commandline are took effect
        for action in m_uvm_applied_cl_action:
            if not action.used:
                # TODO: Error handling
                # `uvm_warning("INVLCMDARGS",$sformatf("\"+uvm_set_action=%s\" never took effect due to a mismatching component pattern",m_uvm_applied_cl_action[idx].arg))
                pass
        for action in m_uvm_applied_cl_sev:
            if not m_uvm_applied_cl_sev.used:
                # TODO: Error handling
                #`uvm_warning("INVLCMDARGS",$sformatf("\"+uvm_set_severity=%s\" never took effect due to a mismatching component pattern",m_uvm_applied_cl_sev[idx].arg))
                pass

        if get_sim_time() > 0:
            # TODO: Error handling
            # `uvm_fatal("RUNPHSTIME", {"The run phase must start at time 0, current time is ",
            #    $sformatf("%0t", $realtime), ". No non-zero delays are allowed before ",
            #    "run_test(), and pre-run user defined phases may not consume ",
            #    "simulation time before the start of the run phase."})
            pass
    
    # -------------
    # At end of elab phase we need to do tlm binding resolution.
    def phase_started(self, phase):
        if phase == end_of_elaboration_ph:
            self.do_resolve_bindings()
            if self.enable_print_topology:
                self.print_topology()
                
            srvr = uvm_report_server.get_server()
            if srvr.get_severity_count(UVM_ERROR) > 0:
                self.uvm_report_fatal("BUILDERR", "stopping due to build errors", UVM_NONE)

    # m_uvm_get_root
    # internal function not to be used
    # get the initialized singleton instance of uvm_root
    @staticmethod
    def m_uvm_get_root():
        if uvm_root.m_inst is None:
            top = uvm_root()
    
        if top != m_inst:
            # Something very, very bad has happened and
            # we already fatal'd.  Throw out the garbage
            # root.
            return None
        
        top.m_domain = uvm_domain.get_uvm_domain();
        
        return uvm_root.m_inst
    

    m_relnotes_done = False

    function void end_of_elaboration_phase(uvm_phase phase);
        uvm_component_proxy p = new("proxy");
        uvm_top_down_visitor_adapter#(uvm_component) adapter = new("adapter");
        uvm_coreservice_t cs = uvm_coreservice_t::get();
        uvm_visitor#(uvm_component) v = cs.get_component_visitor();
        adapter.accept(this, v, p);
    endfunction

#-----------------------------------------------------------------------------
# IMPLEMENTATION
#-----------------------------------------------------------------------------

function void uvm_root::report_header(UVM_FILE file = 0);
    string q[$];
    uvm_report_server srvr;
    uvm_cmdline_processor clp;
    string args[$];

    srvr = uvm_report_server::get_server();
    clp = uvm_cmdline_processor::get_inst();

    if (clp.get_arg_matches("+UVM_NO_RELNOTES", args)) return;

    if (!m_relnotes_done) begin
      q.push_back("\n  ***********       IMPORTANT RELEASE NOTES         ************\n");
      m_relnotes_done = 1;

        q.push_back("\n  This implementation of the UVM Library deviates from the 1800.2-2017\n");
      q.push_back("  standard.  See the DEVIATIONS.md file contained in the release\n");
      q.push_back("  for more details.\n");
          
`ifdef UVM_ENABLE_DEPRECATED_API

      q.push_back("\n  You are using a version of the UVM library that has been compiled\n");
      q.push_back("  with `UVM_ENABLE_DEPRECATED_API defined.\n");
      q.push_back("  See https:#accellera.mantishub.io/view.php?id=5072 for more details.\n");
   
`endif

    end # !m_relnotes_done

    q.push_back("\n----------------------------------------------------------------\n");
    q.push_back({uvm_revision_string(),"\n"});
    q.push_back("\n");
        q.push_back("All copyright owners for this kit are listed in NOTICE.txt\n");
        q.push_back("All Rights Reserved Worldwide\n");
    q.push_back("----------------------------------------------------------------\n");

    if(m_relnotes_done)
        q.push_back("\n      (Specify +UVM_NO_RELNOTES to turn off this notice)\n");

    `uvm_info("UVM/RELNOTES",`UVM_STRING_QUEUE_STREAMING_PACK(q),UVM_LOW)
endfunction


# set_timeout
# -----------

function void uvm_root::set_timeout(time timeout, bit overridable=1);
    static bit m_uvm_timeout_overridable = 1;
    if (m_uvm_timeout_overridable == 0) begin
        uvm_report_info("NOTIMOUTOVR",
            $sformatf("The global timeout setting of %0d is not overridable to %0d due to a previous setting.",
                phase_timeout, timeout), UVM_NONE);
        return;
    end
    m_uvm_timeout_overridable = overridable;
    phase_timeout = timeout;
endfunction

# m_do_verbosity_settings
# -----------------------

function void uvm_root::m_do_verbosity_settings();
    string set_verbosity_settings[$];
    string split_vals[$];
    uvm_verbosity tmp_verb;

    # Retrieve them all into set_verbosity_settings
    void'(clp.get_arg_values("+uvm_set_verbosity=", set_verbosity_settings));

    for(int i = 0; i < set_verbosity_settings.size(); i++) begin
        uvm_split_string(set_verbosity_settings[i], ",", split_vals);
        if(split_vals.size() < 4  or  split_vals.size() > 5) begin
            uvm_report_warning("INVLCMDARGS",
                $sformatf("Invalid number of arguments found on the command line for setting '+uvm_set_verbosity=%s'.  Setting ignored.",
                    set_verbosity_settings[i]), UVM_NONE, "", "");
        end
        # Invalid verbosity
        if(!clp.m_convert_verb(split_vals[2], tmp_verb)) begin
            uvm_report_warning("INVLCMDVERB",
                $sformatf("Invalid verbosity found on the command line for setting '%s'.",
                    set_verbosity_settings[i]), UVM_NONE, "", "");
        end
    end
endfunction


# m_do_timeout_settings
# ---------------------

function void uvm_root::m_do_timeout_settings();
    string timeout_settings[$];
    string timeout;
    string split_timeout[$];
    int timeout_count;
    time timeout_int;
    string override_spec;
    timeout_count = clp.get_arg_values("+UVM_TIMEOUT=", timeout_settings);
    if (timeout_count ==  0)
        return;
    else begin
        timeout = timeout_settings[0];
        if (timeout_count > 1) begin
            string timeout_list;
            string sep;
            for (int i = 0; i < timeout_settings.size(); i++) begin
                if (i != 0)
                    sep = "; ";
                timeout_list = {timeout_list, sep, timeout_settings[i]};
            end
            uvm_report_warning("MULTTIMOUT",
                $sformatf("Multiple (%0d) +UVM_TIMEOUT arguments provided on the command line.  '%s' will be used.  Provided list: %s.",
                    timeout_count, timeout, timeout_list), UVM_NONE);
        end
        uvm_report_info("TIMOUTSET",
            $sformatf("'+UVM_TIMEOUT=%s' provided on the command line is being applied.", timeout), UVM_NONE);
        void'($sscanf(timeout,"%d,%s",timeout_int,override_spec));
        case(override_spec)
            "YES"   : set_timeout(timeout_int, 1);
            "NO"    : set_timeout(timeout_int, 0);
            default : set_timeout(timeout_int, 1);
        endcase
    end
endfunction


# m_do_factory_settings
# ---------------------

function void uvm_root::m_do_factory_settings();
    string args[$];

    void'(clp.get_arg_matches("/^\\+(UVM_SET_INST_OVERRIDE|uvm_set_inst_override)=/",args));
    foreach(args[i]) begin
        m_process_inst_override(args[i].substr(23, args[i].len()-1));
    end
    void'(clp.get_arg_matches("/^\\+(UVM_SET_TYPE_OVERRIDE|uvm_set_type_override)=/",args));
    foreach(args[i]) begin
        m_process_type_override(args[i].substr(23, args[i].len()-1));
    end
endfunction


# m_process_inst_override
# -----------------------

function void uvm_root::m_process_inst_override(string ovr);
    string split_val[$];
    uvm_coreservice_t cs = uvm_coreservice_t::get();
    uvm_factory factory=cs.get_factory();

    uvm_split_string(ovr, ",", split_val);

    if(split_val.size() != 3 ) begin
        uvm_report_error("UVM_CMDLINE_PROC", {"Invalid setting for +uvm_set_inst_override=", ovr,
                ", setting must specify <requested_type>,<override_type>,<instance_path>"}, UVM_NONE);
        return;
    end

    uvm_report_info("INSTOVR", {"Applying instance override from the command line: +uvm_set_inst_override=", ovr}, UVM_NONE);
    factory.set_inst_override_by_name(split_val[0], split_val[1], split_val[2]);
endfunction


# m_process_type_override
# -----------------------

function void uvm_root::m_process_type_override(string ovr);
    string split_val[$];
    int replace=1;
    uvm_coreservice_t cs = uvm_coreservice_t::get();
    uvm_factory factory=cs.get_factory();

    uvm_split_string(ovr, ",", split_val);

    if(split_val.size() > 3  or  split_val.size() < 2) begin
        uvm_report_error("UVM_CMDLINE_PROC", {"Invalid setting for +uvm_set_type_override=", ovr,
                ", setting must specify <requested_type>,<override_type>[,<replace>]"}, UVM_NONE);
        return;
    end

    # Replace arg is optional. If set, must be 0 or 1
    if(split_val.size() == 3) begin
        if(split_val[2]=="0") replace =  0;
        else if (split_val[2] == "1") replace = 1;
        else begin
            uvm_report_error("UVM_CMDLINE_PROC", {"Invalid replace arg for +uvm_set_type_override=", ovr ," value must be 0 or 1"}, UVM_NONE);
            return;
        end
    end

    uvm_report_info("UVM_CMDLINE_PROC", {"Applying type override from the command line: +uvm_set_type_override=", ovr}, UVM_NONE);
    factory.set_type_override_by_name(split_val[0], split_val[1], replace);
endfunction


# m_process_config
# ----------------

function void uvm_root::m_process_config(string cfg, bit is_int);
    uvm_bitstream_t v;
    string split_val[$];
    uvm_root m_uvm_top;
    uvm_coreservice_t cs;
    cs = uvm_coreservice_t::get();
    m_uvm_top = cs.get_root();


    uvm_split_string(cfg, ",", split_val);
    if(split_val.size() == 1) begin
        uvm_report_error("UVM_CMDLINE_PROC", {"Invalid +uvm_set_config command\"", cfg,
                "\" missing field and value: component is \"", split_val[0], "\""}, UVM_NONE);
        return;
    end

    if(split_val.size() == 2) begin
        uvm_report_error("UVM_CMDLINE_PROC", {"Invalid +uvm_set_config command\"", cfg,
                "\" missing value: component is \"", split_val[0], "\"  field is \"", split_val[1], "\""}, UVM_NONE);
        return;
    end

    if(split_val.size() > 3) begin
        uvm_report_error("UVM_CMDLINE_PROC",
            $sformatf("Invalid +uvm_set_config command\"%s\" : expected only 3 fields (component, field and value).", cfg), UVM_NONE);
        return;
    end

    if(is_int) begin
        if(split_val[2].len() > 2) begin
            string base, extval;
            base = split_val[2].substr(0,1);
            extval = split_val[2].substr(2,split_val[2].len()-1);
            case(base)
                "'b" : v = extval.atobin();
                "0b" : v = extval.atobin();
                "'o" : v = extval.atooct();
                "'d" : v = extval.atoi();
                "'h" : v = extval.atohex();
                "'x" : v = extval.atohex();
                "0x" : v = extval.atohex();
                default : v = split_val[2].atoi();
            endcase
        end
        else begin
            v = split_val[2].atoi();
        end
        uvm_report_info("UVM_CMDLINE_PROC", {"Applying config setting from the command line: +uvm_set_config_int=", cfg}, UVM_NONE);
        uvm_config_int::set(m_uvm_top, split_val[0], split_val[1], v);
    end
    else begin
        uvm_report_info("UVM_CMDLINE_PROC", {"Applying config setting from the command line: +uvm_set_config_string=", cfg}, UVM_NONE);
        uvm_config_string::set(m_uvm_top, split_val[0], split_val[1], split_val[2]);
    end

endfunction

# m_process_default_sequence
# ----------------

function void uvm_root::m_process_default_sequence(string cfg);
    string split_val[$];
    uvm_coreservice_t cs = uvm_coreservice_t::get();
    uvm_root m_uvm_top = cs.get_root();
    uvm_factory f = cs.get_factory();
    uvm_object_wrapper w;

    uvm_split_string(cfg, ",", split_val);
    if(split_val.size() == 1) begin
        uvm_report_error("UVM_CMDLINE_PROC", {"Invalid +uvm_set_default_sequence command\"", cfg,
                "\" missing phase and type: sequencer is \"", split_val[0], "\""}, UVM_NONE);
        return;
    end

    if(split_val.size() == 2) begin
        uvm_report_error("UVM_CMDLINE_PROC", {"Invalid +uvm_set_default_sequence command\"", cfg,
                "\" missing type: sequencer is \"", split_val[0], "\"  phase is \"", split_val[1], "\""}, UVM_NONE);
        return;
    end

    if(split_val.size() > 3) begin
        uvm_report_error("UVM_CMDLINE_PROC",
            $sformatf("Invalid +uvm_set_default_sequence command\"%s\" : expected only 3 fields (sequencer, phase and type).", cfg), UVM_NONE);
        return;
    end

    w = f.find_wrapper_by_name(split_val[2]);
    if (w  is None) begin
        uvm_report_error("UVM_CMDLINE_PROC",
            $sformatf("Invalid type '%s' provided to +uvm_set_default_sequence", split_val[2]),
            UVM_NONE);
        return;
    end
    else begin
        uvm_report_info("UVM_CMDLINE_PROC", {"Setting default sequence from the command line: +uvm_set_default_sequence=", cfg}, UVM_NONE);
        uvm_config_db#(uvm_object_wrapper)::set(this, {split_val[0], ".", split_val[1]}, "default_sequence", w);
    end

endfunction : m_process_default_sequence


# m_do_config_settings
# --------------------

function void uvm_root::m_do_config_settings();
    string args[$];

    void'(clp.get_arg_matches("/^\\+(UVM_SET_CONFIG_INT|uvm_set_config_int)=/",args));
    foreach(args[i]) begin
        m_process_config(args[i].substr(20, args[i].len()-1), 1);
    end
    void'(clp.get_arg_matches("/^\\+(UVM_SET_CONFIG_STRING|uvm_set_config_string)=/",args));
    foreach(args[i]) begin
        m_process_config(args[i].substr(23, args[i].len()-1), 0);
    end
    void'(clp.get_arg_matches("/^\\+(UVM_SET_DEFAULT_SEQUENCE|uvm_set_default_sequence)=/", args));
    foreach(args[i]) begin
        m_process_default_sequence(args[i].substr(26, args[i].len()-1));
    end
endfunction


# m_do_max_quit_settings
# ----------------------

function void uvm_root::m_do_max_quit_settings();
    uvm_report_server srvr;
    string max_quit_settings[$];
    int max_quit_count;
    string max_quit;
    string split_max_quit[$];
    int max_quit_int;
    srvr = uvm_report_server::get_server();
    max_quit_count = clp.get_arg_values("+UVM_MAX_QUIT_COUNT=", max_quit_settings);
    if (max_quit_count ==  0)
        return;
    else begin
        max_quit = max_quit_settings[0];
        if (max_quit_count > 1) begin
            string max_quit_list;
            string sep;
            for (int i = 0; i < max_quit_settings.size(); i++) begin
                if (i != 0)
                    sep = "; ";
                max_quit_list = {max_quit_list, sep, max_quit_settings[i]};
            end
            uvm_report_warning("MULTMAXQUIT",
                $sformatf("Multiple (%0d) +UVM_MAX_QUIT_COUNT arguments provided on the command line.  '%s' will be used.  Provided list: %s.",
                    max_quit_count, max_quit, max_quit_list), UVM_NONE);
        end
        uvm_report_info("MAXQUITSET",
            $sformatf("'+UVM_MAX_QUIT_COUNT=%s' provided on the command line is being applied.", max_quit), UVM_NONE);
        uvm_split_string(max_quit, ",", split_max_quit);
        max_quit_int = split_max_quit[0].atoi();
        case(split_max_quit[1])
            "YES"   : srvr.set_max_quit_count(max_quit_int, 1);
            "NO"    : srvr.set_max_quit_count(max_quit_int, 0);
            default : srvr.set_max_quit_count(max_quit_int, 1);
        endcase
    end
endfunction


# m_check_verbosity
# ----------------

function void uvm_root::m_check_verbosity();

    string verb_string;
    string verb_settings[$];
    int verb_count;
    int plusarg;
    int verbosity = UVM_MEDIUM;

  `ifndef UVM_CMDLINE_NO_DPI
    # Retrieve the verbosities provided on the command line.
    verb_count = clp.get_arg_values("+UVM_VERBOSITY=", verb_settings);
  `else
    verb_count = $value$plusargs("UVM_VERBOSITY=%s",verb_string);
    if (verb_count)
        verb_settings.push_back(verb_string);
  `endif

    # If none provided, provide message about the default being used.
    #if (verb_count == 0)
    #  uvm_report_info("DEFVERB", ("No verbosity specified on the command line.  Using the default: UVM_MEDIUM"), UVM_NONE);

    # If at least one, use the first.
    if (verb_count > 0) begin
        verb_string = verb_settings[0];
        plusarg = 1;
    end

    # If more than one, provide the warning stating how many, which one will
    # be used and the complete list.
    if (verb_count > 1) begin
        string verb_list;
        string sep;
        for (int i = 0; i < verb_settings.size(); i++) begin
            if (i != 0)
                sep = ", ";
            verb_list = {verb_list, sep, verb_settings[i]};
        end
        uvm_report_warning("MULTVERB",
            $sformatf("Multiple (%0d) +UVM_VERBOSITY arguments provided on the command line.  '%s' will be used.  Provided list: %s.", verb_count, verb_string, verb_list), UVM_NONE);
    end

    if(plusarg == 1) begin
        case(verb_string)
            "UVM_NONE"    : verbosity = UVM_NONE;
            "NONE"        : verbosity = UVM_NONE;
            "UVM_LOW"     : verbosity = UVM_LOW;
            "LOW"         : verbosity = UVM_LOW;
            "UVM_MEDIUM"  : verbosity = UVM_MEDIUM;
            "MEDIUM"      : verbosity = UVM_MEDIUM;
            "UVM_HIGH"    : verbosity = UVM_HIGH;
            "HIGH"        : verbosity = UVM_HIGH;
            "UVM_FULL"    : verbosity = UVM_FULL;
            "FULL"        : verbosity = UVM_FULL;
            "UVM_DEBUG"   : verbosity = UVM_DEBUG;
            "DEBUG"       : verbosity = UVM_DEBUG;
            default       : begin
                verbosity = verb_string.atoi();
                if(verbosity > 0)
                    uvm_report_info("NSTVERB", $sformatf("Non-standard verbosity value, using provided '%0d'.", verbosity), UVM_NONE);
                if(verbosity == 0) begin
                    verbosity = UVM_MEDIUM;
                    uvm_report_warning("ILLVERB", "Illegal verbosity value, using default of UVM_MEDIUM.", UVM_NONE);
                end
            end
        endcase
    end

    set_report_verbosity_level_hier(verbosity);

endfunction

function void uvm_root::m_check_uvm_field_flag_size();
    if ( (`UVM_FIELD_FLAG_SIZE) < UVM_FIELD_FLAG_RESERVED_BITS ) begin
        uvm_report_fatal( "BAD_FIELD_FLAG_SZ",
            $sformatf(
                "Macro UVM_FIELD_FLAG_SIZE is set to %0d which is less than the required minimum of UVM_FIELD_FLAG_RESERVED_BITS (%0d).",
                `UVM_FIELD_FLAG_SIZE, UVM_FIELD_FLAG_RESERVED_BITS
            )
        );
    end
endfunction



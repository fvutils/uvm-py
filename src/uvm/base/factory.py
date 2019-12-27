#
#------------------------------------------------------------------------------
# Copyright 2007-2014 Mentor Graphics Corporation
# Copyright 2015 Analog Devices, Inc.
# Copyright 2014 Semifore
# Copyright 2017 Intel Corporation
# Copyright 2018 Qualcomm, Inc.
# Copyright 2011 Synopsys, Inc.
# Copyright 2007-2018 Cadence Design Systems, Inc.
# Copyright 2013 Verilab
# Copyright 2013-2018 NVIDIA Corporation
# Copyright 2017 Cisco Systems, Inc.
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
from uvm.base.coreservice import uvm_coreservice_t
from uvm.base.object_globals import UVM_NONE


#typedef struct {uvm_object_wrapper m_type;
#                string             m_type_name;} m_uvm_factory_type_pair_t;
#Instance overrides by requested type lookup
class uvm_factory_queue_class():
    
    def __init__(self):
        self.queue = []

#------------------------------------------------------------------------------
# Title -- NODOCS -- UVM Factory
#
# This page covers the classes that define the UVM factory facility.
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#
# CLASS -- NODOCS -- uvm_factory
#
#------------------------------------------------------------------------------
#
# As the name implies, uvm_factory is used to manufacture (create) UVM objects
# and components. Object and component types are registered
# with the factory using lightweight proxies to the actual objects and
# components being created. The <uvm_object_registry #(T,Tname)> and
# <uvm_component_registry #(T,Tname)> class are used to proxy <uvm_objects>
# and <uvm_components>.
#
# The factory provides both name-based and type-based interfaces.
#
# type-based - The type-based interface is far less prone to errors in usage.
#   When errors do occur, they are caught at compile-time.
#
# name-based - The name-based interface is dominated 
#   by string arguments that can be misspelled and provided in the wrong order.
#   Errors in name-based requests might only be caught at the time of the call,
#   if at all. Further, the name-based interface is not portable across
#   simulators when used with parameterized classes.
#
#
# The ~uvm_factory~ is an abstract class which declares many of its methods
# as ~pure virtual~.  The UVM uses the <uvm_default_factory> class
# as its default factory implementation.
#   
# See <uvm_default_factory::Usage> section for details on configuring and using the factory.
#
  
# @uvm-ieee 1800.2-2017 auto 8.3.1.1
class uvm_factory():

    # Group -- NODOCS -- Retrieving the factory

 
    # @uvm-ieee 1800.2-2017 auto 8.3.1.2.1
    @staticmethod
    def get():
        return uvm_coreservice_t.get().get_factory()
  
    # @uvm-ieee 1800.2-2017 auto 8.3.1.2.2
    @staticmethod
    def set(f):
        uvm_coreservice_t.get().set_factory(f)

    # Group -- NODOCS -- Registering Types

    # Function -- NODOCS -- register
    #
    # Registers the given proxy object, ~obj~, with the factory. The proxy object
    # is a lightweight substitute for the component or object it represents. When
    # the factory needs to create an object of a given type, it calls the proxy's
    # create_object or create_component method to do so.
    #
    # When doing name-based operations, the factory calls the proxy's
    # ~get_type_name~ method to match against the ~requested_type_name~ argument in
    # subsequent calls to <create_component_by_name> and <create_object_by_name>.
    # If the proxy object's ~get_type_name~ method returns the empty string,
    # name-based lookup is effectively disabled.

    # @uvm-ieee 1800.2-2017 auto 8.3.1.3
    def register(self, obj):
        pass


    # Group -- NODOCS -- Type & Instance Overrides

    # Function -- NODOCS -- set_inst_override_by_type

    # @uvm-ieee 1800.2-2017 auto 8.3.1.4.1
    def set_inst_override_by_type(self, original_type, override_type, full_inst_path):
        pass

    # Function -- NODOCS -- set_inst_override_by_name
    #
    # Configures the factory to create an object of the override's type whenever
    # a request is made to create an object of the original type using a context
    # that matches ~full_inst_path~. The original type is typically a super class
    # of the override type.
    #
    # When overriding by type, the ~original_type~ and ~override_type~ are
    # handles to the types' proxy objects. Preregistration is not required.
    #
    # When overriding by name, the ~original_type_name~ typically refers to a
    # preregistered type in the factory. It may, however, be any arbitrary
    # string. Future calls to any of the ~create_*~ methods with the same string
    # and matching instance path will produce the type represented by
    # ~override_type_name~, which must be preregistered with the factory.
    #
    # The ~full_inst_path~ is matched against the concatenation of
    # {~parent_inst_path~, ".", ~name~} provided in future create requests. The
    # ~full_inst_path~ may include wildcards (* and ?) such that a single
    # instance override can be applied in multiple contexts. A ~full_inst_path~
    # of "*" is effectively a type override, as it will match all contexts.
    #
    # When the factory processes instance overrides, the instance queue is
    # processed in order of override registrations, and the first override
    # match prevails. Thus, more specific overrides should be registered
    # first, followed by more general overrides.

    # @uvm-ieee 1800.2-2017 auto 8.3.1.4.1
    def set_inst_override_by_name(self, original_type_name, override_type_name, full_inst_path):
        pass

    # Function -- NODOCS -- set_type_override_by_type

    # @uvm-ieee 1800.2-2017 auto 8.3.1.4.2
    def set_type_override_by_type(self, original_type, override_type, replace=True):
        pass

    # Function -- NODOCS -- set_type_override_by_name
    #
    # Configures the factory to create an object of the override's type whenever
    # a request is made to create an object of the original type, provided no
    # instance override applies. The original type is typically a super class of
    # the override type.
    #
    # When overriding by type, the ~original_type~ and ~override_type~ are
    # handles to the types' proxy objects. Preregistration is not required.
    #
    # When overriding by name, the ~original_type_name~ typically refers to a
    # preregistered type in the factory. It may, however, be any arbitrary
    # string. Future calls to any of the ~create_*~ methods with the same string
    # and matching instance path will produce the type represented by
    # ~override_type_name~, which must be preregistered with the factory.
    #
    # When ~replace~ is 1, a previous override on ~original_type_name~ is
    # replaced, otherwise a previous override, if any, remains intact.

    # @uvm-ieee 1800.2-2017 auto 8.3.1.4.2
    def set_type_override_by_name (self, original_type_name, override_type_name, replace=True):
        pass

    # Group -- NODOCS -- Creation

    # Function -- NODOCS -- create_object_by_type

    # @uvm-ieee 1800.2-2017 auto 8.3.1.5
    def create_object_by_type(self, requested_type, parent_inst_path="", name=""):
        return None

    # Function -- NODOCS -- create_component_by_type

    # @uvm-ieee 1800.2-2017 auto 8.3.1.5
    def create_component_by_type (self, requested_type,  parent_inst_path="", name="", parent=None):
        # Pure virtual
        pass

    # Function -- NODOCS -- create_object_by_name

    # @uvm-ieee 1800.2-2017 auto 8.3.1.5
    def create_object_by_name(self, requested_type_name, parent_inst_path="", name=""):
        # Pure virtual
        pass

    # Function -- NODOCS -- is_type_name_registered
    
    # @uvm-ieee 1800.2-2017 auto 8.3.1.7.3
    def is_type_name_registered(self, type_name):
        # Pure virtual
        pass

 
    # Function -- NODOCS -- is_type_registered 

    # @uvm-ieee 1800.2-2017 auto 8.3.1.7.4
    def is_type_registered(self, obj):
        # Pure virtual
        pass

    
    #
    # Creates and returns a component or object of the requested type, which may
    # be specified by type or by name. A requested component must be derived
    # from the <uvm_component> base class, and a requested object must be derived
    # from the <uvm_object> base class.
    #
    # When requesting by type, the ~requested_type~ is a handle to the type's
    # proxy object. Preregistration is not required.
    #
    # When requesting by name, the ~request_type_name~ is a string representing
    # the requested type, which must have been registered with the factory with
    # that name prior to the request. If the factory does not recognize the
    # ~requested_type_name~, an error is produced and a ~null~ handle returned.
    #
    # If the optional ~parent_inst_path~ is provided, then the concatenation,
    # {~parent_inst_path~, ".",~name~}, forms an instance path (context) that
    # is used to search for an instance override. The ~parent_inst_path~ is
    # typically obtained by calling the <uvm_component::get_full_name> on the
    # parent.
    #
    # If no instance override is found, the factory then searches for a type
    # override.
    #
    # Once the final override is found, an instance of that component or object
    # is returned in place of the requested type. New components will have the
    # given ~name~ and ~parent~. New objects will have the given ~name~, if
    # provided.
    #
    # Override searches are recursively applied, with instance overrides taking
    # precedence over type overrides. If ~foo~ overrides ~bar~, and ~xyz~
    # overrides ~foo~, then a request for ~bar~ will produce ~xyz~. Recursive
    # loops will result in an error, in which case the type returned will be
    # that which formed the loop. Using the previous example, if ~bar~
    # overrides ~xyz~, then ~bar~ is returned after the error is issued.

    # @uvm-ieee 1800.2-2017 auto 8.3.1.5
    def create_component_by_name(self, 
            requested_type_name,  
            parent_inst_path, # =""
            name, 
            parent):
        # Pure virtual
        pass

    # Group -- NODOCS -- Name Aliases
  
    # Function -- NODOCS -- set_type_alias
    # @uvm-ieee 1800.2-2017 auto 8.3.1.6.1
    def set_type_alias(self, alias_type_name, original_type):
        # Pure virtual
        pass
  
    #Intended to allow overrides by type to use the alias_type_name as an additional name to refer to
    #original_type  
  
    # Function -- NODOCS -- set_inst_alias
    # @uvm-ieee 1800.2-2017 auto 8.3.1.6.2
    def set_inst_alias(self, alias_type_name, original_type, full_inst_path):
        pass

    #Intended to allow overrides by name to use the alias_type_name as an additional name to refer to
    #original_type in the context referred to by full_inst_path.  


    # Group -- NODOCS -- Debug

    # Function -- NODOCS -- debug_create_by_type

    def debug_create_by_type(self, requested_type, parent_inst_path="", name=""):
        pass

    # Function -- NODOCS -- debug_create_by_name
    #
    # These methods perform the same search algorithm as the ~create_*~ methods,
    # but they do not create new objects. Instead, they provide detailed
    # information about what type of object it would return, listing each
    # override that was applied to arrive at the result. Interpretation of the
    # arguments are exactly as with the ~create_*~ methods.

    def debug_create_by_name(self, requested_type_name, parent_inst_path="", name=""):
        # Pure virtual
        pass

                   
    # Function -- NODOCS -- find_override_by_type

    # @uvm-ieee 1800.2-2017 auto 8.3.1.7.1
    def find_override_by_type(self, requested_type, full_inst_path):
        pass

    # Function -- NODOCS -- find_override_by_name
    #
    # These methods return the proxy to the object that would be created given
    # the arguments. The ~full_inst_path~ is typically derived from the parent's
    # instance path and the leaf name of the object to be created, i.e.
    # { parent.get_full_name(), ".", name }.
    
    # @uvm-ieee 1800.2-2017 auto 8.3.1.7.1
    def find_override_by_name(self, requested_type_name, full_inst_path):
        pass

    # Function -- NODOCS -- find_wrapper_by_name
    #
    # This method returns the <uvm_object_wrapper> associated with a given
    # ~type_name~.  
    # @uvm-ieee 1800.2-2017 auto 8.3.1.7.2
    def find_wrapper_by_name(self, type_name):
        # Pure virtual
        pass

    # Function -- NODOCS -- print
    #
    # Prints the state of the uvm_factory, including registered types, instance
    # overrides, and type overrides.
    #
    # When ~all_types~ is 0, only type and instance overrides are displayed. When
    # ~all_types~ is 1 (default), all registered user-defined types are printed as
    # well, provided they have names associated with them. When ~all_types~ is 2,
    # the UVM types (prefixed with uvm_) are included in the list of registered
    # types.

    # @uvm-ieee 1800.2-2017 auto 8.3.1.7.5
    def print(self, all_types=True):
        # Pure virtual
        pass
    



#------------------------------------------------------------------------------
#
# Group -- NODOCS -- Usage
#
# Using the factory involves three basic operations
#
# 1 - Registering objects and components types with the factory
# 2 - Designing components to use the factory to create objects or components
# 3 - Configuring the factory with type and instance overrides, both within and
#     outside components
#
# We'll briefly cover each of these steps here. More reference information can
# be found at <Utility Macros>, <uvm_component_registry #(T,Tname)>,
# <uvm_object_registry #(T,Tname)>, <uvm_component>.
#
# 1 -- Registering objects and component types with the factory:
#
# When defining <uvm_object> and <uvm_component>-based classes, simply invoke
# the appropriate macro. Use of macros are required to ensure portability
# across different vendors' simulators.
#
# Objects that are not parameterized are declared as
#
#|  class packet (uvm_object):;
#|    `uvm_object_utils(packet)
#|  endclass
#|
#|  class packetD (packet):;
#|    `uvm_object_utils(packetD)
#|  endclass
#
# Objects that are parameterized are declared as
#
#|  class packet #(type T=int, int WIDTH=32) (uvm_object):;
#|    `uvm_object_param_utils(packet #(T,WIDTH))
#|   endclass
#
# Components that are not parameterized are declared as
#
#|  class comp (uvm_component):;
#|    `uvm_component_utils(comp)
#|  endclass
#
# Components that are parameterized are declared as
#
#|  class comp #(type T=int, int WIDTH=32) (uvm_component):;
#|    `uvm_component_param_utils(comp #(T,WIDTH))
#|  endclass
#
# The `uvm_*_utils macros for simple, non-parameterized classes will register
# the type with the factory and define the get_type, get_type_name, and create
# virtual methods inherited from <uvm_object>. It will also define a static
# type_name variable in the class, which will allow you to determine the type
# without having to allocate an instance. 
#
# The `uvm_*_param_utils macros for parameterized classes differ from
# `uvm_*_utils classes in the following ways:
#
# - The ~get_type_name~ method and static type_name variable are not defined. You
#   will need to implement these manually.
#
# - A type name is not associated with the type when registering with the
#   factory, so the factory's *_by_name operations will not work with
#   parameterized classes.
#
# - The factory's <print>, <debug_create_by_type>, and <debug_create_by_name>
#   methods, which depend on type names to convey information, will list
#   parameterized types as '<unknown>'.
#
# It is worth noting that environments that exclusively use the type-based
# factory methods (*_by_type) do not require type registration. The factory's
# type-based methods will register the types involved "on the fly," when first
# used. However, registering with the `uvm_*_utils macros enables name-based
# factory usage and implements some useful utility functions.
#
#
# 2 -- Designing components that defer creation to the factory:
#
# Having registered your objects and components with the factory, you can now
# make requests for new objects and components via the factory. Using the factory
# instead of allocating them directly (via new) allows different objects to be
# substituted for the original without modifying the requesting class. The
# following code defines a driver class that is parameterized.
#
#|  class driverB #(type T=uvm_object) (uvm_driver):;
#|
#|    # parameterized classes must use the _param_utils version
#|    `uvm_component_param_utils(driverB #(T))
#|
#|    # our packet type; this can be overridden via the factory
#|    T pkt;
#|
#|    # standard component constructor
#|    def __init__(string name, uvm_component parent=None);
#|      super.new(name,parent);
#|    endfunction
#|
#|    # get_type_name not implemented by macro for parameterized classes
#|    static function string type_name();
#|      return {"driverB #(",T::type_name(),")"};
#|    endfunction : type_name
#|    virtual function string get_type_name();
#|      return type_name();
#|    endfunction
#|
#|    # using the factory allows pkt overrides from outside the class
#|    virtual function void build_phase(uvm_phase phase);
#|      pkt = packet::type_id::create("pkt",this);
#|    endfunction
#|
#|    # print the packet so we can confirm its type when printing
#|    virtual function void do_print(uvm_printer printer);
#|      printer.print_object("pkt",pkt);
#|    endfunction
#|
#|  endclass
#
# For purposes of illustrating type and instance overrides, we define two
# subtypes of the ~driverB~ class. The subtypes are also parameterized, so
# we must again provide an implementation for <uvm_object::get_type_name>,
# which we recommend writing in terms of a static string constant.
#
#|  class driverD1 #(type T=uvm_object) (driverB): #(T);
#|
#|    `uvm_component_param_utils(driverD1 #(T))
#|
#|    def __init__(string name, uvm_component parent=None);
#|      super.new(name,parent);
#|    endfunction
#|
#|    static function string type_name();
#|      return {"driverD1 #(",T::type_name,")"};
#|    endfunction : type_name
#|    virtual function string get_type_name();
#|      return type_name();
#|    endfunction
#|
#|  endclass
#|
#|  class driverD2 #(type T=uvm_object) (driverB): #(T);
#|
#|    `uvm_component_param_utils(driverD2 #(T))
#|
#|    def __init__(string name, uvm_component parent=None);
#|      super.new(name,parent);
#|    endfunction
#|
#|    static function string type_name();
#|      return {"driverD2 #(",T::type_name,")"};
#|    endfunction : type_name
#|    virtual function string get_type_name();
#|      return type_name();
#|    endfunction
#|
#|  endclass
#|
#|  # typedef some specializations for convenience
#|  typedef driverB  #(packet) B_driver;   # the base driver
#|  typedef driverD1 #(packet) D1_driver;  # a derived driver
#|  typedef driverD2 #(packet) D2_driver;  # another derived driver
#
# Next, we'll define a agent component, which requires a utils macro for
# non-parameterized types. Before creating the drivers using the factory, we
# override ~driver0~'s packet type to be ~packetD~.
#
#|  class agent (uvm_agent):;
#|
#|    `uvm_component_utils(agent)
#|    ...
#|    B_driver driver0;
#|    B_driver driver1;
#|
#|    def __init__(string name, uvm_component parent=None);
#|      super.new(name,parent);
#|    endfunction
#|
#|    virtual function void build_phase(uvm_phase phase);
#|
#|      # override the packet type for driver0 and below
#|      packet::type_id::set_inst_override(packetD::get_type(),"driver0.*");
#|
#|      # create using the factory; actual driver types may be different
#|      driver0 = B_driver::type_id::create("driver0",this);
#|      driver1 = B_driver::type_id::create("driver1",this);
#|
#|    endfunction
#|
#|  endclass
#
# Finally we define an environment class, also not parameterized. Its ~build_phase~
# method shows three methods for setting an instance override on a grandchild
# component with relative path name, ~agent1.driver1~, all equivalent.
#
#|  class env (uvm_env):;
#|
#|    `uvm_component_utils(env)
#|
#|    agent agent0;
#|    agent agent1;
#|
#|    def __init__(string name, uvm_component parent=None);
#|      super.new(name,parent);
#|    endfunction
#|
#|    virtual function void build_phase(uvm_phase phase);
#|
#|      # three methods to set an instance override for agent1.driver1
#|      # - via component convenience method...
#|      set_inst_override_by_type("agent1.driver1",
#|                                B_driver::get_type(),
#|                                D2_driver::get_type());
#|
#|      # - via the component's proxy (same approach as create)...
#|      B_driver::type_id::set_inst_override(D2_driver::get_type(),
#|                                           "agent1.driver1",this);
#|
#|      # - via a direct call to a factory method...
#|      factory.set_inst_override_by_type(B_driver::get_type(),
#|                                        D2_driver::get_type(),
#|                                        {get_full_name(),".agent1.driver1"});
#|
#|      # create agents using the factory; actual agent types may be different
#|      agent0 = agent::type_id::create("agent0",this);
#|      agent1 = agent::type_id::create("agent1",this);
#|
#|    endfunction
#|
#|    # at end_of_elaboration, print topology and factory state to verify
#|    virtual function void end_of_elaboration_phase(uvm_phase phase);
#|      uvm_top.print_topology();
#|    endfunction
#|
#|    virtual task run_phase(uvm_phase phase);
#|      #100 global_stop_request();
#|    endfunction
#|
#|  endclass
#   
#
# 3 -- Configuring the factory with type and instance overrides:
#
# In the previous step, we demonstrated setting instance overrides and creating
# components using the factory within component classes. Here, we will
# demonstrate setting overrides from outside components, as when initializing
# the environment prior to running the test.
#
#|  module top;
#|
#|    env env0;
#|
#|    initial begin
#|
#|      # Being registered first, the following overrides take precedence
#|      # over any overrides made within env0's construction & build.
#|
#|      # Replace all base drivers with derived drivers...
#|      B_driver::type_id::set_type_override(D_driver::get_type());
#|
#|      # ...except for agent0.driver0, whose type remains a base driver.
#|      #     (Both methods below have the equivalent result.)
#|
#|      # - via the component's proxy (preferred)
#|      B_driver::type_id::set_inst_override(B_driver::get_type(),
#|                                           "env0.agent0.driver0");
#|
#|      # - via a direct call to a factory method
#|      factory.set_inst_override_by_type(B_driver::get_type(),
#|                                        B_driver::get_type(),
#|                                    {get_full_name(),"env0.agent0.driver0"});
#|
#|      # now, create the environment; our factory configuration will
#|      # govern what topology gets created
#|      env0 = new("env0");
#|
#|      # run the test (will execute build phase)
#|      run_test();
#|
#|    end
#|
#|  endmodule
#
# When the above example is run, the resulting topology (displayed via a call to
# <uvm_root::print_topology> in env's <uvm_component::end_of_elaboration_phase> method)
# is similar to the following:
#
#| # UVM_INFO @ 0 [RNTST] Running test ...
#| # UVM_INFO @ 0 [UVMTOP] UVM testbench topology:
#| # ----------------------------------------------------------------------
#| # Name                     Type                Size                Value
#| # ----------------------------------------------------------------------
#| # env0                     env                 -                  env0@2
#| #   agent0                 agent               -                agent0@4
#| #     driver0              driverB #(packet)   -               driver0@8
#| #       pkt                packet              -                  pkt@21
#| #     driver1              driverD #(packet)   -              driver1@14
#| #       pkt                packet              -                  pkt@23
#| #   agent1                 agent               -                agent1@6
#| #     driver0              driverD #(packet)   -              driver0@24
#| #       pkt                packet              -                  pkt@37
#| #     driver1              driverD2 #(packet)  -              driver1@30
#| #       pkt                packet              -                  pkt@39
#| # ----------------------------------------------------------------------
# 
#------------------------------------------------------------------------------








#-----------------------------------------------------------------------------
# IMPLEMENTATION
#-----------------------------------------------------------------------------

# m_debug_create
# --------------

# function void  uvm_default_factory::m_debug_create (string requested_type_name,
#                                             uvm_object_wrapper requested_type,
#                                             string parent_inst_path,
#                                             string name);
# 
#   string full_inst_path;
#   uvm_object_wrapper result;
#   
#   if (parent_inst_path == "")
#     full_inst_path = name;
#   else if (name != "")
#     full_inst_path = {parent_inst_path,".",name};
#   else
#     full_inst_path = parent_inst_path;
# 
#   m_override_info.delete();
# 
#   if (requested_type == null) begin
#     if (!m_type_names.exists(requested_type_name) &&
#       !m_lookup_strs.exists(requested_type_name)) begin
#       uvm_report_warning("Factory Warning", {"The factory does not recognize '",
#         requested_type_name,"' as a registered type."}, UVM_NONE);
#       return;
#     end
#     m_debug_pass = 1;
#     
#     result = find_override_by_name(requested_type_name,full_inst_path);
#   end
#   else begin
#     m_debug_pass = 1;
#     if (!m_types.exists(requested_type))
#       register(requested_type); 
#     result = find_override_by_type(requested_type,full_inst_path);
#     if (requested_type_name == "")
#       requested_type_name = requested_type.get_type_name();
#   end
# 
#   m_debug_display(requested_type_name, result, full_inst_path);
#   m_debug_pass = 0;
# 
#   foreach (m_override_info[index])
#     m_override_info[index].selected = 0;
# 
# endfunction
# 
# 
# # m_debug_display
# # ---------------
# 
# function void  uvm_default_factory::m_debug_display (string requested_type_name,
#                                              uvm_object_wrapper result,
#                                              string full_inst_path);
# 
#   int    max1,max2,max3;
#   string dash = "---------------------------------------------------------------------------------------------------";
#   string space= "                                                                                                   ";
#   string qs[$];
# 
#   qs.push_back("\n#### Factory Override Information (*)\n\n");
#   qs.push_back(
#       $sformatf("Given a request for an object of type '%s' with an instance\npath of '%s' the factory encountered\n\n",
#           requested_type_name,full_inst_path));
# 
#   if (m_override_info.size() == 0)
#     qs.push_back("no relevant overrides.\n\n");
#   else begin
# 
#     qs.push_back("the following relevant overrides. An 'x' next to a match indicates a\nmatch that was ignored.\n\n");
# 
#     foreach (m_override_info[i]) begin
#       if (m_override_info[i].orig.m_type_name.len() > max1)
#         max1=m_override_info[i].orig.m_type_name.len();
#       if (m_override_info[i].full_inst_path.len() > max2)
#         max2=m_override_info[i].full_inst_path.len();
#       if (m_override_info[i].ovrd.m_type_name.len() > max3)
#         max3=m_override_info[i].ovrd.m_type_name.len();
#     end
# 
#     if (max1 < 13) max1 = 13;
#     if (max2 < 13) max2 = 13;
#     if (max3 < 13) max3 = 13;
# 
#     qs.push_back($sformatf("Original Type%0s  Instance Path%0s  Override Type%0s\n", 
#         space.substr(1,max1-13),space.substr(1,max2-13),space.substr(1,max3-13)));
# 
#     qs.push_back($sformatf("  %0s  %0s  %0s\n",dash.substr(1,max1),
#                                dash.substr(1,max2),
#                                dash.substr(1,max3)));
# 
#     foreach (m_override_info[i]) begin
#       qs.push_back($sformatf("%s%0s%0s\n",
#              m_override_info[i].selected ? "  " : "x ",
#              m_override_info[i].orig.m_type_name,
#              space.substr(1,max1-m_override_info[i].orig.m_type_name.len())));
#       qs.push_back($sformatf("  %0s%0s", m_override_info[i].full_inst_path,
#              space.substr(1,max2-m_override_info[i].full_inst_path.len())));
#       qs.push_back($sformatf("  %0s%0s", m_override_info[i].ovrd.m_type_name,
#              space.substr(1,max3-m_override_info[i].ovrd.m_type_name.len())));
#       if (m_override_info[i].full_inst_path == "*")
#         qs.push_back("  <type override>");
#       else
#         qs.push_back("\n");
#     end
#     qs.push_back("\n");
#   end
# 
# 
#   qs.push_back("Result:\n\n");
#   qs.push_back($sformatf("  The factory will produce an object of type '%0s'\n", 
#            result == null ? requested_type_name : result.get_type_name()));
# 
#   qs.push_back("\n(*) Types with no associated type name will be printed as <unknown>\n\n####\n\n");
#   
#   `uvm_info("UVM/FACTORY/DUMP",`UVM_STRING_QUEUE_STREAMING_PACK(qs),UVM_NONE)
# endfunction


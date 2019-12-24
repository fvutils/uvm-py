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
from uvm.base.factory import uvm_factory

#------------------------------------------------------------------------------
#
# CLASS: uvm_default_factory
#
#------------------------------------------------------------------------------
#
# Default implementation of the UVM factory.  The library implements the
# following public API beyond what is documented in IEEE 1800.2.
   
# @uvm-ieee 1800.2-2017 auto 8.3.3
class uvm_default_factory (uvm_factory):

    # Group --NODOCS-- Registering Types

    # Function --NODOCS-- register
    #
    # Registers the given proxy object, ~obj~, with the factory.
   
    def register(self, obj):
        if obj == None:
            # TODO: error handling
#            uvm_report_fatal ("NULLWR", "Attempting to register a null object with the factory", UVM_NONE);
            pass
        
        if obj.get_type_name() != "" and obj.get_type_name() != "<unknown>":
            if self.m_type_names.exists(obj.get_type_name()):
                # TODO: error handling
#                uvm_report_warning("TPRGED", {"Type name '",obj.get_type_name(),
#                    "' already registered with factory. No string-based lookup ",
#                    "support for multiple types with the same type name."}, UVM_NONE);
                pass
            else:
                self.m_type_names[obj.get_type_name()] = obj

        if m_types.exists(obj):
            if obj.get_type_name() != "" and obj.get_type_name() != "<unknown>":
                # TODO: error handling
#                uvm_report_warning("TPRGED", {"Object type '",obj.get_type_name(),
#                         "' already registered with factory. "}, UVM_NONE);
                pass
            else:
                overrides = []
                self.m_types[obj] = True;

                # If a named override happens before the type is registered, need to update
                # the override type
                # Note:Registration occurs via static initialization, which occurs ahead of
                # procedural (e.g. initial) blocks. There should not be any preexisting overrides.
                overrides = {m_type_overrides, m_inst_overrides};
                for i in overrides:
                    if self.m_matches_type_pair(.match_type_pair(overrides[index].orig),
                             .requested_type(null),
                             .requested_type_name(obj.get_type_name()))) begin
                        overrides[i].orig.m_type = obj; 
                        
                    if self.m_matches_type_pair(.match_type_pair(overrides[index].ovrd),
                             .requested_type(null),
                             .requested_type_name(obj.get_type_name())):
                        overrides[i].ovrd.m_type = obj; 


    # Group --NODOCS-- Type & Instance Overrides

    # Function --NODOCS-- set_inst_override_by_type

    def set_inst_override_by_type (self, original_type, override_type, full_inst_path):
        replaced = False
       

        # check that old and new are not the same
        if original_type == override_type:
            if original_type.get_type_name() == "" or original_type.get_type_name() == "<unknown>":
                # TODO: error handling
#                uvm_report_warning("TYPDUP", {"Original and override type ",
#                                    "arguments are identical"}, UVM_NONE);
                pass
            else:
                # TODO: error handling
#                uvm_report_warning("TYPDUP", {"Original and override type ",
#                                    "arguments are identical: ",
#                                    original_type.get_type_name()}, UVM_NONE);
                pass

        # register the types if not already done so, for the benefit of string-based lookup
        if not m_types.exists(original_type):
            self.register(original_type)

        if not m_types.exists(override_type):
            self.register(override_type)


        # check for existing type override
        for override in self.m_type_overrides:
            if self.m_matches_type_override(.override(override),
                               .requested_type(original_type),
                               .requested_type_name(original_type.get_type_name())):
                msg = ""
                # TODO: error handling
#      msg = {"Original object type '",original_type.get_type_name(),
#             "' already registered to produce '",
#             m_type_overrides[index].ovrd.m_type_name,"'"};
                if not replace:
                    msg += ".  Set 'replace' argument to replace the existing entry."
                    # TODO: error handling
#                  uvm_report_info("TPREGD", msg, UVM_MEDIUM);
                    return
                msg += ".  Replacing with override to produce type '",
                    override_type.get_type_name(),"'."
                # TODO: error handling
#               uvm_report_info("TPREGR", msg, UVM_MEDIUM);
                replaced = True
                override.orig.m_type = original_type; 
                override.orig.m_type_name = original_type.get_type_name(); 
                override.ovrd.m_type = override_type; 
                override.ovrd.m_type_name = override_type.get_type_name(); 
                override.replace = replace;
            elif override.orig.m_type == None:
                # due to aliasing, optimizing around type override when the type is unknown could
                #  end up causing the wrong override to be returned as the type for the alias may
                # resolve to match this existing override
                break

        # make a new entry
        if not replaced:
            override = uvm_factory_override(.orig_type(original_type),
                   .orig_type_name(original_type.get_type_name()),
                   .ovrd_type(override_type),
                   .ovrd_type_name(override_type.get_type_name()),
                   .replace(replace))

            self.m_type_overrides.insert(0, override)
        

    # Function --NODOCS-- set_inst_override_by_name
    #
    # Configures the factory to create an object of the override's type whenever
    # a request is made to create an object of the original type using a context
    # that matches ~full_inst_path~. 
    # 
    # ~original_type_name~ may be the factory-registered type name or an aliased name
    # specified with <set_inst_alias> in the context of ~full_inst_path~.
  extern virtual function
      void set_inst_override_by_name (string original_type_name,
                                      string override_type_name,
                                      string full_inst_path);


    # Function --NODOCS-- set_type_override_by_type

  extern virtual function
      void set_type_override_by_type (uvm_object_wrapper original_type,
                                      uvm_object_wrapper override_type,
                                      bit replace=1);

    # Function --NODOCS-- set_type_override_by_name
    #
    # Configures the factory to create an object of the override's type whenever
    # a request is made to create an object of the original type, provided no
    # instance override applies.
    #
    # ~original_type_name~ may be the factory-registered type name or an aliased name
    # specified with <set_type_alias>.
   
  extern virtual function
      void set_type_override_by_name (string original_type_name,
                                      string override_type_name,
                                      bit replace=1);

    # Function --NODOCS-- set_type_alias
    #
    # Intended to allow overrides by type to use the alias_type_name as an additional name to refer to
    # original_type 
  
  extern virtual function
      void set_type_alias(string alias_type_name, 
                          uvm_object_wrapper original_type); 
  
    # Function --NODOCS-- set_inst_alias
    #
    # Intended to allow overrides by name to use the alias_type_name as an additional name to refer to
    # original_type in the context referred to by full_inst_path.  

  extern virtual function
      void set_inst_alias(string alias_type_name,
                          uvm_object_wrapper original_type, string full_inst_path);



    # Group --NODOCS-- Creation

    # Function --NODOCS-- create_object_by_type

  extern virtual function
      uvm_object    create_object_by_type    (uvm_object_wrapper requested_type,  
                                              string parent_inst_path="",
                                              string name=""); 

    # Function --NODOCS-- create_component_by_type

  extern virtual function
      uvm_component create_component_by_type (uvm_object_wrapper requested_type,  
                                              string parent_inst_path="",
                                              string name, 
                                              uvm_component parent);

    # Function --NODOCS-- create_object_by_name

  extern virtual function
      uvm_object    create_object_by_name    (string requested_type_name,  
                                              string parent_inst_path="",
                                              string name=""); 

    # Function --NODOCS-- create_component_by_name
    #
    # Creates and returns a component or object of the requested type, which may
    # be specified by type or by name.
   
  extern virtual function
      uvm_component create_component_by_name (string requested_type_name,  
                                              string parent_inst_path="",
                                              string name, 
                                              uvm_component parent);

    # Function --NODOCS-- is_type_name_registered
    #
    # silently check type with a given name was registered in the factory or not
 
  extern virtual
      function bit is_type_name_registered    (string type_name);

   
    # Function --NODOCS-- is_type_registered
    #
    # silently check type is registered in the factory or not
 
  extern virtual
      function bit is_type_registered    (uvm_object_wrapper obj);


    # Function: debug_create_by_type
    # Debug traces for ~create_*_by_type~ methods.
    #
    # This method performs the same search algorithm as the <create_object_by_type> and
    # <create_component_by_type> methods, however instead of creating the new object or component,
    # the method shall generate a report message detailing how the object or component would
    # have been constructed after all overrides are accounted for.
    #
    # @uvm-accellera The details of this API are specific to the Accellera implementation, and are not being considered for contribution to 1800.2
  extern virtual function
      void debug_create_by_type (uvm_object_wrapper requested_type,
                                 string parent_inst_path="",
                                 string name="");

    # Function: debug_create_by_name
    # Debug traces for ~create_*_by_name~ methods.
    #
    # This method performs the same search algorithm as the <create_object_by_name> and
    # <create_component_by_name> methods, however instead of creating the new object or component,
    # the method shall generate a report message detailing how the object or component would
    # have been constructed after all overrides are accounted for.
    #
    # @uvm-accellera The details of this API are specific to the Accellera implementation, and are not being considered for contribution to 1800.2
  extern virtual function
      void debug_create_by_name (string requested_type_name,
                                 string parent_inst_path="",
                                 string name="");

                   
    # Function --NODOCS-- find_override_by_type

  extern virtual function
      uvm_object_wrapper find_override_by_type (uvm_object_wrapper requested_type,
                                                string full_inst_path);

    # Function --NODOCS-- find_override_by_name
    #
    # These methods return the proxy to the object that would be created given
    # the arguments.
   
  extern virtual function
      uvm_object_wrapper find_override_by_name (string requested_type_name,
                                                string full_inst_path);

  extern virtual 
    function uvm_object_wrapper find_wrapper_by_name            (string type_name);

    # Function --NODOCS-- print
    #
    # Prints the state of the uvm_factory, including registered types, instance
    # overrides, and type overrides.
    #
  extern  virtual function void print (int all_types=1);


    #----------------------------------------------------------------------------
    # PRIVATE MEMBERS
  
  extern protected
      function void  m_debug_create (string requested_type_name,
                                     uvm_object_wrapper requested_type,
                                     string parent_inst_path,
                                     string name);
  
  extern protected
      function void  m_debug_display(string requested_type_name,
                                     uvm_object_wrapper result,
                                     string full_inst_path);

  extern  
      function uvm_object_wrapper m_resolve_type_name(string requested_type_name);
   
  extern  
      function uvm_object_wrapper m_resolve_type_name_by_inst(string requested_type_name,
                                                              string full_inst_path);   

  extern 
      function bit m_matches_type_pair(m_uvm_factory_type_pair_t match_type_pair,
                                       uvm_object_wrapper requested_type,
                                       string requested_type_name);
   
  extern 
      function bit m_matches_type_override(uvm_factory_override override,
                                           uvm_object_wrapper requested_type,
                                           string requested_type_name,
                                           string full_inst_path="",
                                           bit match_original_type = 1,
                                           bit resolve_null_type_by_inst=0);
  extern 
      function bit m_matches_inst_override(uvm_factory_override override,
                                           uvm_object_wrapper requested_type,
                                           string requested_type_name,
                                           string full_inst_path="");
   
  typedef struct  {
    m_uvm_factory_type_pair_t orig;
    string alias_type_name;
    string full_inst_path;
  } m_inst_typename_alias_t;
    
  protected bit                      m_types[uvm_object_wrapper];
  protected bit                      m_lookup_strs[string];
  protected uvm_object_wrapper       m_type_names[string];
  protected m_inst_typename_alias_t  m_inst_aliases[$];

  protected uvm_factory_override m_type_overrides[$];
  protected uvm_factory_override m_inst_overrides[$];


  local uvm_factory_override     m_override_info[$];
  local static bit m_debug_pass;


  extern function bit check_inst_override_exists
                                      (uvm_object_wrapper original_type,
                                       string original_type_name,
                                       uvm_object_wrapper override_type,
                                       string override_type_name,
                                       string full_inst_path);

endclass


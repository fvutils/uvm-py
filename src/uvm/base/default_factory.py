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
from uvm.base.factory_override import uvm_factory_override
from uvm.base.globals import uvm_report_fatal, uvm_report_warning,\
    uvm_report_info, uvm_report_error, uvm_is_match
from uvm.base.object_globals import UVM_NONE, UVM_MEDIUM, UVM_HIGH
from uvm.util.format import strcat, sformatf


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
    
    def __init__(self):
        super().__init__()
        self.m_types = {} # map<uvm_object_wrapper,bit> TODO: really a set
        self.m_lookup_strs = {} # map<uvm_object_wrapper,bit> TODO: really a set
        self.m_type_names = {} # map<string,uvm_object_wrapper> 
        self.m_inst_aliases = [] # list of m_inst_typename_alias_t
        self.m_type_overrides = [] # list of uvm_factory_override
        self.m_inst_overrides = [] # list of uvm_factory_override
        self.m_override_info = [] # list of uvm_factory_override
        
    # Group --NODOCS-- Registering Types

    # Function --NODOCS-- register
    #
    # Registers the given proxy object, ~obj~, with the factory.
   
    def register(self, obj):
        if obj == None:
            uvm_report_fatal ("NULLWR", "Attempting to register a null object with the factory", UVM_NONE)
            pass
        
        if obj.get_type_name() != "" and obj.get_type_name() != "<unknown>":
            if obj in self.m_type_names.keys():
                uvm_report_warning("TPRGED", strcat("Type name '",obj.get_type_name(),
                    "' already registered with factory. No string-based lookup ",
                    "support for multiple types with the same type name."), UVM_NONE)
            else:
                self.m_type_names[obj.get_type_name()] = obj

        if obj in self.m_types.keys():
            if obj.get_type_name() != "" and obj.get_type_name() != "<unknown>":
                uvm_report_warning("TPRGED", strcat("Object type '",obj.get_type_name(),
                         "' already registered with factory. "), UVM_NONE)
            else:
                self.m_types[obj] = True;

                # If a named override happens before the type is registered, need to update
                # the override type
                # Note:Registration occurs via static initialization, which occurs ahead of
                # procedural (e.g. initial) blocks. There should not be any preexisting overrides.
                overrides = self.m_type_overrides + self.m_inst_overrides
                
                for override in overrides:
                    if self.m_matches_type_pair(override.orig, None, obj.get_type_name()):
                        override.orig.m_type = obj; 
                        
                    if self.m_matches_type_pair(override.ovrd, None, obj.get_type_name()):
                        override.ovrd.m_type = obj; 


    # Group --NODOCS-- Type & Instance Overrides

    # Function --NODOCS-- set_inst_override_by_type

    def set_inst_override_by_type (self, original_type, override_type, full_inst_path):
        # register the types if not already done so
        if not original_type in self.m_types.keys():
            self.register(original_type)

        if not override_type in self.m_types.keys():
            self.register(override_type)

        if self.check_inst_override_exists(original_type,
                                 original_type.get_type_name(),
                                 override_type,
                                 override_type.get_type_name(),
                                 full_inst_path):
            return

        override = uvm_factory_override(
            full_inst_path=full_inst_path,
            orig_type=original_type,
            orig_type_name=original_type.get_type_name(),
            ovrd_type=override_type,
            ovrd_type_name=override_type.get_type_name())

        self.m_inst_overrides.append(override)
        

    # Function --NODOCS-- set_inst_override_by_name
    #
    # Configures the factory to create an object of the override's type whenever
    # a request is made to create an object of the original type using a context
    # that matches ~full_inst_path~. 
    # 
    # ~original_type_name~ may be the factory-registered type name or an aliased name
    # specified with <set_inst_alias> in the context of ~full_inst_path~.
    def set_inst_override_by_name(self, original_type_name, override_type_name, full_inst_path):
        if original_type_name in self.m_type_names.keys():
            original_type = self.m_type_names[original_type_name]

        if override_type_name in self.m_type_names.keys():
            override_type = self.m_type_names[override_type_name]

    # check that type is registered with the factory
#  aliasing feature makes this check invalid.  Aliases
#  aren't resolved until find/creation time so the type
#  may resolve differently depending on the instance. 
#  if (override_type == null) begin
#    uvm_report_error("TYPNTF", {"Cannot register instance override with type name '",
#    original_type_name,"' and instance path '",full_inst_path,"' because the type it's supposed ",
#    "to produce, '",override_type_name,"', is not registered with the factory."}, UVM_NONE);
#    return;
#  end

        if original_type == None:
            self.m_lookup_strs[original_type_name] = True

        override = uvm_factory_override(
            full_inst_path,
            original_type_name,
            original_type,
            override_type,
            override_type_name)
  
        if self.check_inst_override_exists(original_type,
                                 original_type_name,
                                 override_type,
                                 override_type_name,
                                 full_inst_path):
            return
        
        self.m_inst_overrides.append(override)


    # Function --NODOCS-- set_type_override_by_type

    def set_type_override_by_type(self, original_type, override_type, replace=True):
        replaced = False
       

        # check that old and new are not the same
        if original_type == override_type:
            if original_type.get_type_name() == "" or original_type.get_type_name() == "<unknown>":
                uvm_report_warning("TYPDUP", strcat("Original and override type ",
                                    "arguments are identical"), UVM_NONE);
            else:
                uvm_report_warning("TYPDUP", strcat("Original and override type ",
                                    "arguments are identical: ",
                                    original_type.get_type_name()), UVM_NONE);

        # register the types if not already done so, for the benefit of string-based lookup
        if not original_type in self.m_types.keys():
            self.register(original_type)

        if not override_type in self.m_types.keys():
            self.register(override_type)


        # check for existing type override
        for override in self.m_type_overrides:
            if self.m_matches_type_override(override, original_type, original_type.get_type_name()):
                msg = strcat("Original object type '",original_type.get_type_name(),
                    "' already registered to produce '",
                    override.ovrd.m_type_name,"'")
                
                if not replace:
                    msg += ".  Set 'replace' argument to replace the existing entry."
                    uvm_report_info("TPREGD", msg, UVM_MEDIUM)
                    return
                msg += ".  Replacing with override to produce type '"
                msg += override_type.get_type_name()
                msg += "'."
                
                uvm_report_info("TPREGR", msg, UVM_MEDIUM)
                
                replaced = True
                override.orig.m_type = original_type
                override.orig.m_type_name = original_type.get_type_name()
                override.ovrd.m_type = override_type
                override.ovrd.m_type_name = override_type.get_type_name()
                override.replace = replace
            elif override.orig.m_type == None:
                # due to aliasing, optimizing around type override when the type is unknown could
                #  end up causing the wrong override to be returned as the type for the alias may
                # resolve to match this existing override
                break

        # make a new entry
        if not replaced:
            override = uvm_factory_override(
                    "",
                    original_type.get_type_name(),
                    original_type,
                    override_type,
                    override_type.get_type_name(),
                    replace)

            self.m_type_overrides.insert(0, override)        

    # Function --NODOCS-- set_type_override_by_name
    #
    # Configures the factory to create an object of the override's type whenever
    # a request is made to create an object of the original type, provided no
    # instance override applies.
    #
    # ~original_type_name~ may be the factory-registered type name or an aliased name
    # specified with <set_type_alias>.
   
    def set_type_override_by_name(self, original_type_name, override_type_name, replace=True):
        replaced = False
  
        original_type = None
        override_type = None

        if original_type_name in self.m_type_names.keys():
            original_type = self.m_type_names[original_type_name]

        if override_type_name in self.m_type_names.keys():
            override_type = self.m_type_names[override_type_name]


    # check that type is registered with the factory
#  aliasing feature makes this check invalid.  Aliases
#  aren't resolved until find/creation time so the type
#  may resolve differently depending on the instance. 
#  if (override_type == null) begin
#      uvm_report_error("TYPNTF", {"Cannot register override for original type '",
#      original_type_name,"' because the override type '",
#      override_type_name, "' is not registered with the factory."}, UVM_NONE);
#    return;
#  end

        # check that old and new are not the same
        if original_type_name == override_type_name:
            uvm_report_warning("TYPDUP", strcat("Requested and actual type name ",
                " arguments are identical: ",original_type_name,". Ignoring this override."), UVM_NONE)
            return

        for override_t in self.m_type_overrides:
            if self.m_matches_type_override(override=override_t,
                                   requested_type=original_type,
                                   requested_type_name=original_type_name):
                if not replace:
                    uvm_report_info("TPREGD", strcat("Original type '",original_type_name, "'/'", override_t.orig.m_type_name,
                        "' already registered to produce '",override_t.ovrd.m_type_name,
                        "'.  Set 'replace' argument to replace the existing entry."), UVM_MEDIUM)
                    return
                
                uvm_report_info("TPREGR", strcat("Original object type '",original_type_name, "'/'", override_t.orig.m_type_name,
                    "' already registered to produce '", override_t.ovrd.m_type_name,
                    "'.  Replacing with override to produce type '",override_type_name,"'."), UVM_MEDIUM)
                replaced = True
                override_t.ovrd.m_type = override_type
                override_t.ovrd.m_type_name = override_type_name
                override_t.replace = replace
               
            elif override_t.orig.m_type == None or original_type == None:
                # due to aliasing, optimizing around type override when the type is unknown could
                # end up causing the wrong override to be returned as the type for the alias may
                # resolve to match this existing override
                break
    
        if original_type == None:
            self.m_lookup_strs[original_type_name] = True
    
        if not replaced:
            override = uvm_factory_override(
                full_inst_path="",
                orig_type=original_type,
                orig_type_name=original_type_name,
                ovrd_type=override_type,
                ovrd_type_name=override_type_name,
                replace=replace)
    
            self.m_type_overrides.insert(override)
        

    # Function --NODOCS-- set_type_alias
    #
    # Intended to allow overrides by type to use the alias_type_name as an additional name to refer to
    # original_type 
  
    def set_type_alias(self, alias_type_name, original_type):
        if not self.is_type_registered(original_type):
            uvm_report_warning("BDTYP", strcat("Cannot define alias of type '",
                original_type.get_type_name(),"' because it is not registered with the factory."), UVM_NONE)
        else:
            if not alias_type_name in self.m_type_names.keys():
                
                self.m_type_names[alias_type_name] = original_type
                # If a named override happens before the type alias is set, need to update
                # the override type
                overrides = self.m_type_overrides + self.m_inst_overrides
                
                for override in overrides:
                    if self.m_matches_type_pair(match_type_pair=override.orig, requested_type=None, requested_type_name=alias_type_name):
                        override.orig.m_type = original_type
                    if self.m_matches_type_pair( match_type_pair=override.ovrd, requested_type=None, requested_type_name=alias_type_name):
                        override.ovrd.m_type = original_type        
  
    # Function --NODOCS-- set_inst_alias
    #
    # Intended to allow overrides by name to use the alias_type_name as an additional name to refer to
    # original_type in the context referred to by full_inst_path.  

    def set_inst_alias(self, alias_type_name, original_type, full_inst_path):
        original_type_name = original_type.get_type_name()
    
        if not self.is_type_registered(original_type):
            uvm_report_warning("BDTYP", strcat("Cannot define alias of type '",
                original_type_name,"' because it is not registered with the factory."), UVM_NONE)
        else:
            print("TODO: add aliases to factory")
#             orig_type_alias_per_inst.alias_type_name = alias_type_name
#             orig_type_alias_per_inst.full_inst_path = full_inst_path
#             orig_type_alias_per_inst.orig.m_type_name = original_type_name
#             orig_type_alias_per_inst.orig.m_type = original_type
#             self.m_inst_aliases.append(orig_type_alias_per_inst)      
            pass


    # Group --NODOCS-- Creation

    # Function --NODOCS-- create_object_by_type

    def create_object_by_type(self, requested_type, parent_inst_path="", name=""):

        if parent_inst_path == "":
            full_inst_path = name
        elif name != "":
            full_inst_path = parent_inst_path+"."+name
        else:
            full_inst_path = parent_inst_path

        self.m_override_info.clear()

        requested_type = self.find_override_by_type(requested_type, full_inst_path)

        return requested_type.create_object(name)

    # Function --NODOCS-- create_component_by_type
    def create_component_by_type(self, 
            requested_type,  
            parent_inst_path, # ="",
            name, 
            parent):

        if parent_inst_path == "":
            full_inst_path = name
        elif name != "":
            full_inst_path = parent_inst_path+"."+name
        else:
            full_inst_path = parent_inst_path

        self.m_override_info.clear()

        requested_type = self.find_override_by_type(requested_type, full_inst_path)

        return requested_type.create_component(name, parent)
        

    # Function --NODOCS-- create_object_by_name

    def create_object_by_name(self, requested_type_name, parent_inst_path="", name=""):
        if parent_inst_path == "":
            inst_path = name
        elif name != "":
            inst_path = parent_inst_path+"."+name
        else:
            inst_path = parent_inst_path

        self.m_override_info.clear()

        wrapper = self.find_override_by_name(requested_type_name, inst_path)

        # if no override exists, try to use requested_type_name directly
        if wrapper is None:
            wrapper = self.m_resolve_type_name_by_inst(requested_type_name,inst_path)
        if wrapper is None:
            uvm_report_warning("BDTYP", "Cannot create an object of type '"+
                    requested_type_name+"' because it is not registered with the factory.", UVM_NONE)
            return None

        return wrapper.create_object(name)        

    # Function --NODOCS-- create_component_by_name
    #
    # Creates and returns a component or object of the requested type, which may
    # be specified by type or by name.
   
    def create_component_by_name (self, 
            requested_type_name,  
            parent_inst_path, # ="",
            name, 
            parent):

        if (parent_inst_path == ""):
            inst_path = name
        elif name != "":
            inst_path = strcat(parent_inst_path,".",name)
        else:
            inst_path = parent_inst_path

        self.m_override_info.clear()

        wrapper = self.find_override_by_name(requested_type_name, inst_path)

        # if no override exists, try to use requested_type_name directly
        if wrapper is None:
            if requested_type_name not in self.m_type_names.keys():
                uvm_report_warning("BDTYP", "Cannot create a component of type '"+
                    requested_type_name+"' because it is not registered with the factory.", UVM_NONE)
                return None
            wrapper = self.m_type_names[requested_type_name]

        return wrapper.create_component(name, parent)

    # Function --NODOCS-- is_type_name_registered
    #
    # silently check type with a given name was registered in the factory or not
 
    def is_type_name_registered(self, type_name):
        return type_name in self.m_type_names.keys() 

   
    # Function --NODOCS-- is_type_registered
    #
    # silently check type is registered in the factory or not
 
    def is_type_registered(self, obj):
        return obj in self.m_types.keys()


    # Function: debug_create_by_type
    # Debug traces for ~create_*_by_type~ methods.
    #
    # This method performs the same search algorithm as the <create_object_by_type> and
    # <create_component_by_type> methods, however instead of creating the new object or component,
    # the method shall generate a report message detailing how the object or component would
    # have been constructed after all overrides are accounted for.
    #
    # @uvm-accellera The details of this API are specific to the Accellera implementation, and are not being considered for contribution to 1800.2
    def debug_create_by_type(self, requested_type, parent_inst_path="", name=""):
        self.m_debug_create("", requested_type, parent_inst_path, name)

    # Function: debug_create_by_name
    # Debug traces for ~create_*_by_name~ methods.
    #
    # This method performs the same search algorithm as the <create_object_by_name> and
    # <create_component_by_name> methods, however instead of creating the new object or component,
    # the method shall generate a report message detailing how the object or component would
    # have been constructed after all overrides are accounted for.
    #
    # @uvm-accellera The details of this API are specific to the Accellera implementation, and are not being considered for contribution to 1800.2
    def debug_create_by_name(self, requested_type_name, parent_inst_path="", name=""):
        self.m_debug_create(requested_type_name, None, parent_inst_path, name)

                   
    # Function --NODOCS-- find_override_by_type
    def find_override_by_type(self, requested_type, full_inst_path):
        lindex = None
  
        for override in self.m_override_info:
            if override.orig.m_type == requested_type:
                uvm_report_error("OVRDLOOP", "Recursive loop detected while finding override.", UVM_NONE)
                override.used += 1
                if not self.m_debug_pass:
                    self.debug_create_by_type (requested_type, full_inst_path)
                return requested_type
            if full_inst_path != "":
                for override_i in self.m_inst_overrides:
                    if self.m_matches_inst_override(
                                override=override_i,
                                requested_type=requested_type,
                                requested_type_name=requested_type.get_type_name(),
                                full_inst_path=full_inst_path):
                        self.m_override_info.append(override_i)
                        
                        if lindex is None:
                            lindex = override_i
                            if not self.m_debug_pass:
                                break

        if lindex is None or self.m_debug_pass:
            matched_overrides = []
            
            # type override - exact match
            for override_t in self.m_type_overrides:
                if self.m_matches_type_override(
                    override=override_t,
                    requested_type=requested_type,
                    requested_type_name=requested_type.get_type_name(),
                    full_inst_path=full_inst_path,
                    resolve_null_type_by_inst=True):
                    
                    matched_overrides.append(override_t)
                    
                    if lindex is None or not lindex.replace:
                        lindex = override_t
                        # if override was done with replace == 1, then
                        # it has priority over overrides added before it.
                        # if override was done with replace == 0, then
                        # must continue to looked for an override added before
                        # it that would have higher priority
                        if not self.m_debug_pass and lindex.replace:
                            break
                        
        if len(matched_overrides) != 0:
            if self.m_debug_pass:
                # TODO: join semantics
                self.m_override_info += matched_overrides
            else:
                # TODO: append-all semantics
                print("TODO: append-all semantics")
#                self.m_override_info.append(matched_overrides[$])
  
        if lindex is not None:
            override = lindex.ovrd.m_type
    
            lindex.used += 1
            
            if self.m_debug_pass:
                lindex.selected = True
    
            if not self.m_matches_type_override(
                override=lindex,
                requested_type=requested_type,
                requested_type_name=requested_type.get_type_name(),
                full_inst_path=full_inst_path,
                match_original_type=False,
                resolve_null_type_by_inst=True):
                
                if override is None:
                    override = self.find_override_by_name(lindex.ovrd.m_type_name,full_inst_path)
                else:
                    override = self.find_override_by_type(override,full_inst_path);
                    
            elif override is None:
                override = self.m_resolve_type_name_by_inst(lindex.ovrd.m_type_name,full_inst_path)
                
            if override is None:
                uvm_report_error("TYPNTF", "Cannot resolve override for original type '"+
                        lindex.orig.m_type_name+"' because the override type '"+
                        lindex.ovrd.m_type_name+"' is not registered with the factory.", UVM_NONE)

            return override
        
        # No override found
        return requested_type

    # Function --NODOCS-- find_override_by_name
    #
    # These methods return the proxy to the object that would be created given
    # the arguments.
   
    def find_override_by_name (self, requested_type_name, full_inst_path):
        lindex = None
      
        rtype = self.m_resolve_type_name_by_inst(requested_type_name,full_inst_path)

        if full_inst_path != "":
            for override_i in self.m_inst_overrides:
                if self.m_matches_inst_override(
                    override=override_i,
                    requested_type=rtype,
                    requested_type_name=requested_type_name,
                    full_inst_path=full_inst_path):
                    self.m_override_info.append(override_i)
                    
                    if lindex is None:
                        lindex = override_i
                        
                        if not self.m_debug_pass:
                            break

        if lindex is None or self.m_debug_pass:
            matched_overrides = []
            
            # type override - exact match
            for override_t in self.m_type_overrides:
                if self.m_matches_type_override(
                    override=override_t,
                    requested_type=rtype,
                    requested_type_name=requested_type_name,
                    full_inst_path=full_inst_path,
                    resolve_null_type_by_inst=True):
                    matched_overrides.append(override_t)
                
                if lindex is None or not lindex.replace:
                    lindex = override_t
                    
                    # if override was done with replace == 1, then
                    # it has priority over overrides added before it.
                    # if override was done with replace == 0, then
                    # must continue to looked for an override added before
                    # it that would have higher priority
                    if not self.m_debug_pass and lindex.replace:
                        break
                    
            if len(matched_overrides) > 0:
                if self.m_debug_pass:
                    # TODO: join semantics
                    self.m_override_info += matched_overrides
                else:
                    # TODO: join semantics
                    print("TODO: join semantics")
#                    self.m_override_info.append(matched_overrides[$])
                    pass
  
        if lindex is not None:
            override = lindex.ovrd.m_type
    
            lindex.used += 1
            
            if self.m_debug_pass:
                lindex.selected = True
    
            if not self.m_matches_type_override(
                override=lindex,
                requested_type=rtype,
                requested_type_name=requested_type_name,
                full_inst_path=full_inst_path,
                match_original_type=False,
                resolve_null_type_by_inst=True):
                
                if override is None:
                    override = self.find_override_by_name(lindex.ovrd.m_type_name,full_inst_path)
                else:
                    override = self.find_override_by_type(override,full_inst_path)
                    
            elif override is None:
                override = self.m_resolve_type_name_by_inst(lindex.ovrd.m_type_name,full_inst_path)

            if override is None:
                uvm_report_error("TYPNTF", strcat("Cannot resolve override for original type '",
                    lindex.orig.m_type_name+"' because the override type '",
                    lindex.ovrd.m_type_name+ "' is not registered with the factory."), UVM_NONE)
                
            return override

        # No override found
        return None

    def find_wrapper_by_name(self, type_name):
        wrapper = self.m_resolve_type_name(type_name)
        
        if wrapper is not None:
            return wrapper
        
        uvm_report_warning("UnknownTypeName", strcat("find_wrapper_by_name: Type name '",type_name,
            "' not registered with the factory."), UVM_NONE)

    # Function --NODOCS-- print
    #
    # Prints the state of the uvm_factory, including registered types, instance
    # overrides, and type overrides.
    #
    def print(self, all_types=1):
#  string key;
#  string qs[$];
        key = ""
        qs = []  

        qs.append("\n#### Factory Configuration (*)\n\n")

        # print instance overrides
        if len(self.m_type_overrides) == 0 and len(self.m_inst_overrides) == 0:
            qs.append("  No instance or type overrides are registered with this factory\n")
        else:
            max1=0
            max2=0
            max3=0
        
            dash = "---------------------------------------------------------------------------------------------------"
            space= "                                                                                                   "

            # print instance overrides
            if len(self.m_inst_overrides) == 0:
                qs.append("No instance overrides are registered with this factory\n")
            else:
                for override in self.m_inst_overrides:
                    if len(override.orig.m_type_name) > max1:
                        max1=len(override.orig.m_type_name)
                    if len(override.full_inst_path) > max2:
                        max2=len(override.full_inst_path)
                    if len(override.ovrd.m_type_name) > max3:
                        max3=len(override.ovrd.m_type_name)
                    
                if max1 < 14:
                    max1 = 14
                if max2 < 13:
                    max2 = 13
                if max3 < 13:
                    max3 = 13
    
                qs.append("Instance Overrides:\n\n")
                qs.append(sformatf("  %0s%0s  %0s%0s  %0s%0s\n","Requested Type",space[1:max1-14],
                                              "Override Path", space[1:max2-13],
                                              "Override Type", space[1:max3-13]))
                qs.append(sformatf("  %0s  %0s  %0s\n",dash[1:max1],
                                     dash[1:max2],
                                     dash[1:max3]))
    
                for override in self.m_inst_overrides:
                    qs.append(sformatf("  %0s%0s  %0s%0s", override.orig.m_type_name,
                                       space[1:max1-len(override.orig.m_type_name)],
                                       override.full_inst_path,
                                       space[1:max2-len(override.full_inst_path)]))
                    qs.append(sformatf("  %0s\n",     override.ovrd.m_type_name))
    
            # print type overrides
            if len(self.m_type_overrides) == 0:
                qs.append("\nNo type overrides are registered with this factory\n")
            else:
                # Resize for type overrides
                if max1 < 14:
                    max1 = 14
                if max2 < 13:
                    max2 = 13
                if max3 < 13:
                    max3 = 13
    
                for override in self.m_type_overrides:
                    if len(override.orig.m_type_name) > max1:
                        max1=len(override.orig.m_type_name)
                    if len(override.ovrd.m_type_name) > max2:
                        max2=len(override.ovrd.m_type_name)
    
                if max1 < 14: 
                    max1 = 14
                if max2 < 13: 
                    max2 = 13
                    
                qs.append("\nType Overrides:\n\n")
                qs.append(sformatf("  %0s%0s  %0s%0s\n","Requested Type",space[1:max1-14],
                                      "Override Type", space[1:max2-13]));
                qs.append(sformatf("  %0s  %0s\n",dash[1:max1],
                                dash[1:max2]));
    
                for override in reversed(self.m_type_overrides):
                    qs.append(sformatf("  %0s%0s  %0s\n",
                        override.orig.m_type_name,
                        space[1:max1-len(override.orig.m_type_name)],
                        override.ovrd.m_type_name))
    
            # print all registered types, if all_types >= 1 
            if all_types >= 1 and len(self.m_type_names) > 0:
                banner=False
                qs.append(sformatf("\nAll types registered with the factory: %0d total\n",len(self.m_types)))
    
                print("TODO: debug")
    #             for key in self.m_type_names.keys():
    #             
    #                 # filter out uvm_ classes (if all_types<2) and non-types (lookup strings)
    #                 if all_types >= 2 and uvm_is_match("uvm_", (!(all_types < 2 and uvm_is_match("uvm_*", self.m_type_names[key].get_type_name())) and key == self.m_type_names[key].get_type_name()):
    #                     if not banner:
    #                         qs.append("  Type Name\n")
    #                         qs.append("  ---------\n")
    #                         banner=True
    #                     qs.append(sformatf("  %s\n", self.m_type_names[key].get_type_name()))
    
            qs.append("(*) Types with no associated type name will be printed as <unknown>\n\n####\n\n")
    
            print("TODO: uvm_info " + str(qs))
            # TODO: report
    #        `uvm_info("UVM/FACTORY/PRINT",`UVM_STRING_QUEUE_STREAMING_PACK(qs),UVM_NONE)
        
    #----------------------------------------------------------------------------
    # PRIVATE MEMBERS
  
    def m_debug_create(self, requested_type_name, requested_type, parent_inst_path, name):
        print("TODO: m_debug_create")
        return None
  
    def m_debug_display(self, requested_type_name, result, full_inst_path):
        print("TODO: m_debug_display")
        return None

    def m_resolve_type_name(self, requested_type_name):
        if requested_type_name in self.m_type_names.keys():
            return self.m_type_names[requested_type_name]
        else:
            return None
   
    def m_resolve_type_name_by_inst(self, requested_type_name, full_inst_path):
        wrapper = None

        # TODO: find with
        print("TODO: find with")
#        type_alias_inst = m_inst_aliases.find(i) with ((i.alias_type_name == requested_type_name) && uvm_is_match(i.full_inst_path,full_inst_path))
#         
#         if len(type_alias_inst) > 0:
#             wrapper = type_alias_inst[0].orig.m_type
#         else:
#             wrapper = self.m_resolve_type_name(requested_type_name)
  
        return wrapper

    def m_matches_type_pair(self, 
                            match_type_pair, 
                            requested_type, 
                            requested_type_name):
        return (match_type_pair.m_type is not None and match_type_pair.m_type == requested_type) or (match_type_pair.m_type_name != "<unknown>" and match_type_pair.m_type_name != "" and match_type_pair.m_type_name == requested_type_name)
   
    def m_matches_type_override(self, override, requested_type,
                                requested_type_name,
                                full_inst_path="",
                                match_original_type=True,
                                resolve_null_type_by_inst=False):

        if match_original_type:
            match_type_pair = override.orig
        else:
            match_type_pair = override.ovrd
            
        if match_type_pair.m_type is None:
            if resolve_null_type_by_inst:
                match_type_pair.m_type = self.m_resolve_type_name_by_inst(match_type_pair.m_type_name,full_inst_path)
            else:
                match_type_pair.m_type = self.m_resolve_type_name(match_type_pair.m_type_name)
                
        return self.m_matches_type_pair(
            match_type_pair=match_type_pair,
            requested_type=requested_type,
            requested_type_name=requested_type_name)
                                           
    def m_matches_inst_override(self, override, requested_type, requested_type_name, full_inst_path=""):
        match_type_pair = override.orig
        
        if match_type_pair.m_type is None:
            match_type_pair.m_type = self.m_resolve_type_name_by_inst(
                match_type_pair.m_type_name, full_inst_path)
            
        if self.m_matches_type_pair(
            match_type_pair=match_type_pair,
            requested_type=requested_type,
            requested_type_name=requested_type_name):
            
            if override.has_wildcard:
                if override.full_inst_path == "*" or uvm_is_match(override.full_inst_path,full_inst_path):
                    return True
                else:
                    return False
            else:
                if override.full_inst_path == full_inst_path:
                    return True
                else:
                    return False
                
        return False
  
    # TODO:
#   typedef struct  {
#     m_uvm_factory_type_pair_t orig;
#     string alias_type_name;
#     string full_inst_path;
#   } m_inst_typename_alias_t;
    
  
    m_debug_pass = False


    def check_inst_override_exists(self, original_type, original_type_name, 
            override_type, override_type_name, full_inst_path):

        for override in self.m_inst_overrides:
            if override.full_inst_path == full_inst_path and override.orig.m_type == original_type and override.orig.m_type_name == original_type_name and override.ovrd.m_type == override_type and override.ovrd.m_type_name == override_type_name:
                uvm_report_info("DUPOVRD",strcat("Instance override for '",
                    original_type_name,"' already exists: override type '",
                    override_type_name,"' with full_inst_path '",
                    full_inst_path,"'"),UVM_HIGH)
                return True
        return False




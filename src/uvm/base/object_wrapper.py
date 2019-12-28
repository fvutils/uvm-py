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

#------------------------------------------------------------------------------
#
# CLASS -- NODOCS -- uvm_object_wrapper
#
# The uvm_object_wrapper provides an abstract interface for creating object and
# component proxies. Instances of these lightweight proxies, representing every
# <uvm_object>-based and <uvm_component>-based object available in the test
# environment, are registered with the <uvm_factory>. When the factory is
# called upon to create an object or component, it finds and delegates the
# request to the appropriate proxy.
#
#------------------------------------------------------------------------------

# @uvm-ieee 1800.2-2017 auto 8.3.2.1
class uvm_object_wrapper():
    
    def __init__(self, T):
        self.T = T

    # Function -- NODOCS -- create_object
    #
    # Creates a new object with the optional ~name~.
    # An object proxy (e.g., <uvm_object_registry #(T,Tname)>) implements this
    # method to create an object of a specific type, T.

    # @uvm-ieee 1800.2-2017 auto 8.3.2.2.1
    def create_object(self, name=""):
        if name == "":
            return self.T()
        else:
            return self.T(name)

    # Function -- NODOCS -- create_component
    #
    # Creates a new component, passing to its constructor the given ~name~ and
    # ~parent~. A component proxy (e.g. <uvm_component_registry #(T,Tname)>)
    # implements this method to create a component of a specific type, T.

    # @uvm-ieee 1800.2-2017 auto 8.3.2.2.2
    def create_component(self, name, parent):
        return self.T(name, parent)


    # Function -- NODOCS -- get_type_name
    # 
    # Derived classes implement this method to return the type name of the object
    # created by <create_component> or <create_object>. The factory uses this
    # name when matching against the requested type in name-based lookups.

    # @uvm-ieee 1800.2-2017 auto 8.3.2.2.3
    def get_type_name(self):
        return self.T.__name__

    def initialize(self):
        pass

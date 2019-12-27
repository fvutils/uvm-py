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
#   "License"); you may not use self file except in
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
# CLASS- uvm_factory_override
#
# Internal class.
#------------------------------------------------------------------------------

class uvm_factory_override():
   
    def __init__(self,
                full_inst_path, # =""
                orig_type_name, # = ""
                orig_type, # =None
                ovrd_type,
                ovrd_type_name, # =""
                replace=False):
      
        self.full_inst_path   = full_inst_path
        self.orig = (orig_type, orig_type_name)
        self.ovrd = (ovrd_type, ovrd_type_name)
        self.replace          = replace
        self.has_wildcard     = self.m_has_wildcard(full_inst_path)
        self.used             = 0
        self.selected         = False
        
    def m_has_wildcard(self, nm):
        for c in nm:
            if c == "*" or c == "?":
                return True
        return False
  
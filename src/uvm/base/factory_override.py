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
# CLASS- uvm_factory_override
#
# Internal class.
#------------------------------------------------------------------------------

class uvm_factory_override;
   
  string full_inst_path;
  m_uvm_factory_type_pair_t orig;
  m_uvm_factory_type_pair_t ovrd;
  bit replace;
  bit selected;
  int unsigned used;
  bit has_wildcard;
   
  def __init__ (string full_inst_path="",
                string orig_type_name="",
                uvm_object_wrapper orig_type=None,
                uvm_object_wrapper ovrd_type,
                string ovrd_type_name="",
                bit replace=0);
      
    this.full_inst_path= full_inst_path;
    this.orig.m_type_name = orig_type_name;
    this.orig.m_type      = orig_type;
    this.ovrd.m_type_name = ovrd_type_name;
    this.ovrd.m_type      = ovrd_type;
    this.replace          = replace;
    this.has_wildcard     = m_has_wildcard(full_inst_path); 
  endfunction
  
  function bit m_has_wildcard(string nm);
    foreach (nm[i]) 
      if(nm[i] == "*" || nm[i] == "?") return 1;
    return 0;
  endfunction
  
  
endclass

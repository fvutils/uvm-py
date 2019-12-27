#
#----------------------------------------------------------------------
# Copyright 2018 Cadence Design Systems, Inc.
# Copyright 2018 NVIDIA Corporation
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

# @uvm-ieee 1800.2-2017 auto F.6.1
class uvm_run_test_callback(): # (uvm_callback):;

    # @uvm-ieee 1800.2-2017 auto F.6.2.1
    # @uvm-ieee 1800.2-2017 auto F.7.1.1
    def __init__(self, name="uvm_run_test_callback"):
        pass

    # @uvm-ieee 1800.2-2017 auto F.6.2.2
    def pre_run_test(self):
        pass

    # @uvm-ieee 1800.2-2017 auto F.6.2.3
    def post_run_test(self):
        pass

    # @uvm-ieee 1800.2-2017 auto F.6.2.4
    def pre_abort(self):
        pass

    # @uvm-ieee 1800.2-2017 auto F.6.2.5
    @staticmethod
    def add(cb):
        if not cb in uvm_run_test_callback.m_registered_cbs:
            uvm_run_test_callback.m_registered_cbs.append(cb)
            return True
        else:
            return False

    # @uvm-ieee 1800.2-2017 auto F.6.2.6
    @staticmethod
    def delete(cb):
        return uvm_run_test_callback.m_registered_cbs.remove(cb)

    # 
    # Implementation details.
    # 

    # These functions executes pre_run_test, post_run_test, and pre_abort routines for all registered
    # callbacks.  These are not user functions.  Only uvm_root should call these.
    @staticmethod
    def m_do_pre_run_test():
        for cb in uvm_run_test_callback.m_registered_cbs:
            cb.pre_run_test()
    
    @staticmethod
    def m_do_post_run_test():
        for cb in uvm_run_test_callback.m_registered_cbs:
            cb.post_run_test()
    
    @staticmethod
    def  m_do_pre_abort():
        for cb in uvm_run_test_callback.m_registered_cbs:
            cb.pre_abort()
        pass

    m_registered_cbs = [] # list of uvm_run_test_callback



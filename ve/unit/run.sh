#!/bin/bash

script_dir=`dirname $0`
script_dir=`cd $script_dir; pwd`
uvm_dir=$script_dir

for i in 1 2; do
  uvm_dir=`dirname $uvm_dir`
done

export PYTHONPATH=${uvm_dir}/src

#valgrind --tool=memcheck python3 -m unittest ${@:1}
# gdb --args python3 -m unittest ${@:1}
${uvm_dir}/packages/python/bin/python3 -m unittest ${@:1}



import os
from setuptools import setup

setup(
  name = "uvm-py",
  packages=['uvm'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("uvm-py provides a Python implementation of the Univeral Verification Methodology (UVM)"),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "cocotb"],
  url = "https://github.com/fvutils/uvm-py",
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[
    'cocotb',
  ],
)


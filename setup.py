
import os
from setuptools import setup

setup(
  name = "py-uvm",
  packages=['uvm'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("py-uvm provides a Python implementation of the Univeral Verification Methodology (UVM)"),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "CocoTB"],
  url = "https://github.com/fvutils/py-uvm",
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[
    'cocotb',
  ],
)


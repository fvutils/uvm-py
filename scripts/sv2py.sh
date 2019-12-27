#!/bin/sh

file=$1

if test ! -f $file; then
  echo "Error: file $file doesn't exist"
  exit 1
fi

sed -i \
  -e 's%//%#%g' \
  -e 's%^  #%    #%g' \
  -e 's%extends \([a-zA-Z_][a-zA-Z0-9_]*\)%(\1):%g' \
  -e 's%function new%def __init__%g' \
  -e 's%==null% is None%g' \
  -e 's%== null% is None%g' \
  -e 's%else if%elif:%g' \
  -e 's%&&% and %g' \
  -e 's%||% or %g' \
  -e 's%push_back%append%g' \
  -e 's%delete()%clear()%g' \
  -e 's%=null%=None%g' \
  -e 's%\.\([a-zA-Z_][a-zA-Z0-9_ ]*\)(\([a-zA-Z_][a-zA-Z0-9_ ]*\))%\1=\2%g' \
  $file


#!/usr/bin/env bash


#
# Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
#


targets=(./setup.py ./ic.py ./intellicoder)


pylint "${targets[@]}" \
       --disable=wrong-import-position,invalid-name,too-few-public-methods,bad-builtin,missing-docstring,redefined-variable-type,fixme,too-many-arguments

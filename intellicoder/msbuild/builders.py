"""
Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>

This file is part of IntelliCoder.

IntelliCoder is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

IntelliCoder is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with IntelliCoder.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import division, absolute_import, print_function
from logging import getLogger
import os
from itertools import chain
from subprocess import CalledProcessError


from ..init import _
from ..utils import replace_ext
from .locators import VSPath, VCPath, SDKPath


logging = getLogger(__name__)


class Builder(object):
    """
    Represent a builder.
    """
    def __init__(self):
        self.vs = VSPath()
        self.sdk = SDKPath(self.vs.sdk_dir, self.vs.sdk_version)
        self.vc = VCPath(self.vs.vc_dir, self.sdk)

    def build(self, filenames, cl_args=None, link_args=None,
              x64=False, out_dir=''):
        """
        Compile source files and link object files.
        """
        if not cl_args:
            cl_args = []
        if not link_args:
            link_args = []
        msvc, lib = self.vc.get_bin_and_lib(x64)
        lib = self.make_lib(lib)
        if out_dir:
            cl_args.append('/Fo:' + out_dir + '\\')
        include = self.make_inc(self.vc.inc + self.sdk.inc)
        cl_args.extend(include + filenames)
        try:
            msvc.run_cl('/c', *cl_args)
        except CalledProcessError as error:
            logging.error(_('failed to compile: %s'), filenames)
            logging.error(_('cl.exe returned:\n%s'), error.output)
            return False
        link_args.extend(lib + self.make_objs(filenames, out_dir))
        try:
            msvc.run_link(*link_args)
        except CalledProcessError as error:
            logging.error(_('failed to link: %s'), filenames)
            logging.error(_('link.exe returned:\n%s'), error.output)
            return False
        return True

    def native_build(self, filenames, cl_args=None, link_args=None,
                     x64=False, out_dir=''):
        """
        Compile source files and link object files
        to native binaries.
        """
        if not cl_args:
            cl_args = []
        if not link_args:
            link_args = []
        cl_args.append('/D_AMD64_' if x64 else '/D_X86_')
        link_args.extend(
            ['/driver', '/entry:DriverEntry',
             '/subsystem:native', '/defaultlib:ntoskrnl'])
        msvc, lib = self.vc.get_bin_and_lib(x64, native=True)
        lib = self.make_lib(lib)
        if out_dir:
            cl_args.append('/Fo:' + out_dir + '\\')
        inc = self.make_inc(
            self.sdk.inc + self.sdk.get_inc(native=True)
        )
        cl_args.extend(filenames + inc)
        try:
            msvc.run_cl('/c', *cl_args)
        except CalledProcessError as error:
            logging.error(_('failed to compile: %s'), filenames)
            logging.error(_('cl.exe returned:\n%s'), error.output)
            return False
        link_args.extend(lib + self.make_objs(filenames, out_dir))
        try:
            msvc.run_link(*link_args)
        except CalledProcessError as error:
            logging.error(_('failed to link: %s'), filenames)
            logging.error(_('link.exe returned:\n%s'), error.output)
            return False
        return True

    @staticmethod
    def make_inc(incs):
        """
        Make include directory for link.exe.
        """
        inc_args = [['/I', inc] for inc in incs]
        return list(chain.from_iterable(inc_args))

    @staticmethod
    def make_lib(libs):
        """
        Make lib directory for link.exe.
        """
        lib_args = ['/libpath:' + lib for lib in libs]
        return lib_args

    @staticmethod
    def make_objs(names, out_dir=''):
        """
        Make object file names for cl.exe and link.exe.
        """
        objs = [replace_ext(name, '.obj') for name in names]
        if out_dir:
            objs = [os.path.join(out_dir, obj) for obj in objs]
        return objs


def local_build(native, *args, **kwargs):
    """
    Compile source files and link object files.
    """
    method = 'native_build' if native else 'build'
    logging.debug(_('build type: %s'), method)
    return getattr(Builder(), method)(*args, **kwargs)

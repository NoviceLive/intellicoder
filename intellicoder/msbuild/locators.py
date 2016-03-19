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
import re
from functools import partial
from collections import namedtuple

try:
    from six.moves.winreg import (
        HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, OpenKey, QueryValueEx
    )
    WINREG = True
except ImportError:
    WINREG = False

from ..init import _
from ..utils import is_64_bit, read_file, run_program


logging = getLogger(__name__)


class VCPath(object):
    """
    Path information retrieval of VC
    given VC directory.
    """
    def __init__(self, vc_dir, sdk):
        self.vc_dir = vc_dir
        self.sdk = sdk
        self.inc = self.get_inc()
        self.lib = self.get_lib()
        self.lib64 = self.get_lib('x64')
        if is_64_bit():
            self.bin32 = self.get_bin('amd64_x86')
            self.bin64 = self.get_bin('amd64')
        else:
            self.bin32 = self.get_bin('x86')
            self.bin64 = self.get_bin('x86_amd64')

    def get_bin(self, arch='x86'):
        """
        Get binaries of Visual C++.
        """
        bin_dir = os.path.join(self.vc_dir, 'bin')
        if arch == 'x86':
            arch = ''
        cl_path = os.path.join(bin_dir, arch, 'cl.exe')
        link_path = os.path.join(bin_dir, arch, 'link.exe')
        ml_name = 'ml.exe'
        if arch in ['x86_amd64', 'amd64']:
            ml_name = 'ml64.exe'
        ml_path = os.path.join(bin_dir, arch, ml_name)
        if os.path.isfile(cl_path) \
           and os.path.isfile(link_path) \
           and os.path.isfile(ml_path):
            logging.info(_('using cl.exe: %s'), cl_path)
            logging.info(_('using link.exe: %s'), link_path)
            logging.info(_('using %s: %s'), ml_name, ml_path)
            run_cl = partial(run_program, cl_path)
            run_link = partial(run_program, link_path)
            run_ml = partial(run_program, ml_path)
            return self.Bin(run_cl, run_link, run_ml)
        logging.debug(_('cl.exe not found: %s'), cl_path)
        logging.debug(_('link.exe not found: %s'), link_path)
        logging.debug(_('%s not found: %s'), ml_name, ml_path)
        return self.Bin(None, None, None)

    def get_inc(self):
        """
        Get include directories of Visual C++.
        """
        dirs = []
        for part in ['', 'atlmfc']:
            include = os.path.join(self.vc_dir, part, 'include')
            if os.path.isdir(include):
                logging.info(_('using include: %s'), include)
                dirs.append(include)
            else:
                logging.debug(_('include not found: %s'), include)
        return dirs

    def get_lib(self, arch='x86'):
        """
        Get lib directories of Visual C++.
        """
        if arch == 'x86':
            arch = ''
        if arch == 'x64':
            arch = 'amd64'
        lib = os.path.join(self.vc_dir, 'lib', arch)
        if os.path.isdir(lib):
            logging.info(_('using lib: %s'), lib)
            return [lib]
        logging.debug(_('lib not found: %s'), lib)
        return []

    def get_bin_and_lib(self, x64=False, native=False):
        """
        Get bin and lib.
        """
        if x64:
            msvc = self.bin64
            paths = self.lib64
        else:
            msvc = self.bin32
            paths = self.lib
        if native:
            arch = 'x64' if x64 else 'x86'
            paths += self.sdk.get_lib(arch, native=True)
        else:
            attr = 'lib64' if x64 else 'lib'
            paths += getattr(self.sdk, attr)
        return msvc, paths

    Bin = namedtuple('Bin', ['run_cl', 'run_link', 'run_ml'])


class SDKPath(object):
    """
    Path information retrieval of SDK
    given SDK directory and version.
    """
    def __init__(self, sdk_dir, version):
        self.sdk_dir = sdk_dir
        self.sdk_version = version
        self.inc = self.get_inc()
        self.lib = self.get_lib()
        self.lib64 = self.get_lib('x64')

    def get_inc(self, native=False):
        """
        Get include directories of Windows SDK.
        """
        if self.sdk_version == 'v7.0A':
            include = os.path.join(self.sdk_dir, 'include')
            if os.path.isdir(include):
                logging.info(_('using include: %s'), include)
                return [include]
            logging.debug(_('include not found: %s'), include)
            return []
        if self.sdk_version == 'v8.1':
            dirs = []
            if native:
                parts = ['km', os.path.join('km', 'crt'), 'shared']
            else:
                parts = ['um', 'winrt', 'shared']
            for part in parts:
                include = os.path.join(self.sdk_dir, 'include', part)
                if os.path.isdir(include):
                    logging.info(_('using include: %s'), include)
                    dirs.append(include)
                else:
                    logging.debug(_('inc not found: %s'), include)
            return dirs
        if self.sdk_version == 'v10.0':
            dirs = []
            extra = os.path.join('include', '10.0.10240.0')
            for mode in ['um', 'ucrt', 'shared', 'winrt']:
                include = os.path.join(self.sdk_dir, extra, mode)
                if os.path.isdir(include):
                    logging.info(_('using include: %s'), include)
                    dirs.append(include)
                else:
                    logging.debug(_('inc not found: %s'), include)
            return dirs
        message = 'unknown sdk version: {}'.format(self.sdk_version)
        raise RuntimeError(message)

    def get_lib(self, arch='x86', native=False):
        """
        Get lib directories of Windows SDK.
        """
        if self.sdk_version == 'v7.0A':
            if arch == 'x86':
                arch = ''
            lib = os.path.join(self.sdk_dir, 'lib', arch)
            if os.path.isdir(lib):
                logging.info(_('using lib: %s'), lib)
                return [lib]
            logging.debug(_('lib not found: %s'), lib)
            return []
        if self.sdk_version == 'v8.1':
            if native:
                extra = os.path.join('winv6.3', 'km')
            else:
                extra = os.path.join('winv6.3', 'um')
            lib = os.path.join(self.sdk_dir, 'lib', extra, arch)
            if os.path.isdir(lib):
                logging.info(_('using lib: %s'), lib)
                return [lib]
            logging.debug(_('lib not found: %s'), lib)
            return []
        if self.sdk_version == 'v10.0':
            dirs = []
            extra = os.path.join('lib', '10.0.10240.0')
            for mode in ['um', 'ucrt']:
                lib = os.path.join(self.sdk_dir, extra, mode, arch)
                if os.path.isdir(lib):
                    logging.info(_('using lib: %s'), lib)
                    dirs.append(lib)
                else:
                    logging.debug(_('lib not found: %s'), lib)
            return dirs
        message = 'unknown sdk version: {}'.format(self.sdk_version)
        raise RuntimeError(message)


class VSPath(object):
    """
    Path information retrieval of Visual Studio
    using environment variables.
    """
    def __init__(self):
        self.tool_dir = self.get_tool_dir()
        self.vs_dir = self.get_vs_dir_from_tool_dir()
        self.vc_dir = self.get_vc_dir_from_vs_dir()
        self.sdk_version = self.get_sdk_version()
        self.sdk_dir = self.get_sdk_dir()

    @staticmethod
    def get_tool_dir():
        """
        Get the directory of Visual Studio
        from environment variables.
        """
        def _is_comntools(name):
            return re.match(r'vs\d+comntools', name.lower())

        def _get_version_from_name(name):
            return (re.search(r'\d+', name).group(0), name)

        names = [name for name in os.environ if _is_comntools(name)]
        logging.debug(_('found vscomntools: %s'), names)
        versions = [_get_version_from_name(name) for name in names]
        logging.debug(_('extracted versions: %s'), versions)
        try:
            version = max(versions)
        except ValueError:
            raise OSError(_('Failed to find the VSCOMNTOOLS. '
                            'Have you installed Visual Studio?'))
        else:
            logging.info(_('using version: %s'), version)
            vscomntools = os.environ[version[1]]
            logging.info(_('using vscomntools: %s'), vscomntools)
            return vscomntools

    def get_vs_dir_from_tool_dir(self):
        """
        Get the directory of Visual Studio
        from the directory Tools.
        """
        index = self.tool_dir.find(r'Common7\Tools')
        return self.tool_dir[:index]

    def get_vc_dir_from_vs_dir(self):
        """
        Get Visual C++ directory from Visual Studio directory.
        """
        vc_dir = os.path.join(self.vs_dir, 'vc')
        if os.path.isdir(vc_dir):
            logging.info(_('using vc: %s'), vc_dir)
            return vc_dir
        logging.debug(_('vc not found: %s'), vc_dir)
        return ''

    def get_sdk_version(self):
        """Get the version of Windows SDK
        from VCVarsQueryRegistry.bat."""
        name = 'VCVarsQueryRegistry.bat'
        path = os.path.join(self.tool_dir, name)
        batch = read_file(path)
        if not batch:
            raise RuntimeError(_('failed to find the SDK version'))
        regex = r'(?<=\\Microsoft SDKs\\Windows\\).+?(?=")'
        try:
            return re.search(regex, batch).group()
        except AttributeError:
            return ''


    def get_sdk_dir(self):
        """Get the directory of Windows SDK from registry."""
        if not WINREG:
            return ''
        path = r'\Microsoft\Microsoft SDKs\Windows'
        for node in ['SOFTWARE', r'SOFTWARE\Wow6432Node']:
            for hkey in [HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER]:
                sub_key = node + path + '\\' + self.sdk_version
                try:
                    key = OpenKey(hkey, sub_key)
                except OSError:
                    logging.debug(_('key not found: %s'), sub_key)
                    continue
                else:
                    logging.info(_('using key: %s'), sub_key)
                    value_name = 'InstallationFolder'
                    try:
                        value = QueryValueEx(key, value_name)
                    except OSError:
                        return ''
                    logging.info(_('using dir: %s'), value[0])
                    return value[0]
        return ''

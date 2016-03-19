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
from glob import glob
from itertools import chain
import os
import sys
import platform
from subprocess import check_output

from .init import _


logging = getLogger(__name__)


def run_program(program, *args):
    """Wrap subprocess.check_output to make life easier."""
    real_args = [program]
    real_args.extend(args)
    logging.debug(_('check_output arguments: %s'), real_args)
    check_output(real_args, universal_newlines=True)


def read_file(filename):
    """Read a file."""
    logging.debug(_('Reading file: %s'), filename)
    try:
        with open(filename) as readable:
            return readable.read()
    except OSError:
        logging.error(_('Error reading file: %s'), filename)
        return ''


def get_parent_dir(name):
    """Get the parent directory of a filename."""
    parent_dir = os.path.dirname(os.path.dirname(name))
    if parent_dir:
        return parent_dir
    return os.path.abspath('.')


def glob_many(names):
    """Apply glob.glob to a list of filenames."""
    return list(chain.from_iterable([glob(name) for name in names]))


def is_64_bit():
    """Determine whether the system is 64-bit of not."""
    machine = platform.machine().lower()
    return machine in ['x86_64', 'amd64']


def is_windows():
    """Determine whether the system is Windows or not."""
    return sys.platform == 'win32'


def replace_ext(filename, ext, basename=True):
    """Replace the extension."""
    return split_ext(filename, basename)[0] + ext


def split_ext(path, basename=True):
    """Wrap them to make life easier."""
    if basename:
        path = os.path.basename(path)
    return os.path.splitext(path)


def ad_hoc_magic_from_file(filename, mime=True):
    """Ad-hoc emulation of magic.from_file from python-magic."""
    with open(filename, 'rb') as stream:
        head = stream.read(16)
        if head[:4] == b'\x7fELF':
            return b'application/x-executable'
        elif head[:2] == b'MZ':
            return b'application/x-dosexec'
        else:
            raise NotImplementedError()


def expand_path(*paths):
    """Expand the path with the directory of the executed file."""
    return os.path.join(
        os.path.dirname(os.path.realpath(sys.argv[0])), *paths)


def expand_user(*paths):
    """Wrap the os.path.expanduser to make life easier."""
    return os.path.expanduser(os.path.join('~', *paths))


def remove_false(iterable):
    """Remove False value from the iterable."""
    return filter(bool, iterable)


class AttrsGetter(object):
    """Get attributes from objects."""
    def __init__(self, objects, join=True):
        self.objects = objects
        self.join = join

    def __getattr__(self, name):
        """Get an attribute from multiple objects."""
        logging.debug(_('name: %s'), name)
        attrs = [getattr(one, name) for one in self.objects]
        if isinstance(attrs[0], str) and self.join:
            return ''.join(attrs)
        return attrs

    def get_attrs(self, *names):
        """Get multiple attributes from multiple objects."""
        attrs = [getattr(self, name) for name in names]
        return attrs

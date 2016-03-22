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


import os
from logging import getLogger

try:
    from plumbum.cmd import gcc, ld
except ImportError:
    pass

from .init import _
from .utils import expand_path


logging = getLogger(__name__)


class Builder(object):
    def __init__(self):
        pass

    def build(self, filenames, x64, src, out):
        logging.debug(_('Received files: %s'), filenames)
        filenames = [os.path.join(src, one) for one in filenames]
        if src:
            one = filenames[0]
            another = os.path.join(os.path.dirname(one), 'syscall.c')
            logging.debug(_('Extra source: %s'), another)
            filenames.append(another)
        logging.debug(_('Compiling files: %s'))
        self._compile(filenames, x64, out)
        self._link()


class LinuxBuilder(Builder):
    def _compile(self, filenames, x64, out):
        arch = '-m64' if x64 else '-m32'
        include = expand_path('intellicoder', 'share', 'rawsc')
        logging.debug(_('Extra include: %s'), include)
        gcc(arch, filenames, '-I', include, '-o', out, '-I', '.')

    def _link(self):
        ld('--version')

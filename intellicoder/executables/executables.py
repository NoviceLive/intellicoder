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


from logging import getLogger

try:
    from magic import from_file as magic_from_file
except ImportError:
    raise RuntimeError('sudo pip install python-magic')

from .elf import ELF
from .pe import PE
from ..i18n import _


logging = getLogger(__name__)


class Executable(object):
    """Binary Executables."""
    def __init__(self, stream):
        self.mime = magic_from_file(stream.name, mime=True)
        logging.debug(_('MIME type: %s'), self.mime)

        if self.mime in [
                b'application/x-executable',
                b'application/x-sharedlib']:
            self.binary = ELF(stream)
            self.system = 'linux'
            self.prefix = 'elf'
        elif self.mime == b'application/x-mach-binary':
            raise NotImplementedError(self.mime)
        elif self.mime == b'application/x-dosexec':
            self.binary = PE(stream)
            self.system = 'windows'
            self.prefix = 'pe'
        else:
            raise NotImplementedError(self.mime)

    def get_section_data(self, *args, **kwargs):
        """Get the data of the section."""
        return self.binary.get_section_data(*args, **kwargs)

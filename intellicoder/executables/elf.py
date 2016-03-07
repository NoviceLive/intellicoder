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
    from elftools.elf.elffile import ELFFile as ELFBackend
except ImportError:
    pass

from ..i18n import _


logging = getLogger(__name__)


class ELF(object):
    """ELF file."""
    def __init__(self, stream):
        try:
            self.binary = ELFBackend(stream)
        except NameError:
            raise RuntimeError(_('Install pyelftools!'))

    def get_section_data(self, name):
        """Get the data of the section."""
        logging.debug(_('Obtaining ELF section: %s'), name)
        section = self.binary.get_section_by_name(name)
        if section:
            return section.data()
        else:
            logging.error(_('Section no found: %s'), name)
            return b''

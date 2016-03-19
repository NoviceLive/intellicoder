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
import sys

try:
    from pefile import PE as PEBackend
    PEFILE = True
except ImportError:
    PEFILE = False

from ..init import _
from ..utils import AttrsGetter


logging = getLogger(__name__)


class PE(object):
    """PE file."""
    def __init__(self, stream):
        try:
            self.binary = PEBackend(stream.name)
        except NameError:
            logging.critical(_('Install pefile!'))
            sys.exit(1)

    def get_section_data(self, name):
        """Get the data of the section."""
        logging.debug(_('Obtaining PE section: %s'), name)
        for section in self.binary.sections:
            if section.Name.rstrip(b'\x00') == name:
                return section.get_data()
        return b''

    def get_export_table(self):
        """Get the export table."""
        symbols = self.binary.DIRECTORY_ENTRY_EXPORT.symbols
        names = AttrsGetter(symbols, join=False).name
        return names

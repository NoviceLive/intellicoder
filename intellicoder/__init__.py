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


from logging import Handler, getLogger
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(Handler):
        def emit(self, record):
            pass

from colorama import init

from .converters import Converter
from .executables import Executable
from .database import Database


__all__ = ['Converter', 'Executable']


__author__ = 'Gu Zhengxiong'
__version__ = '0.5.0'


PROGRAM_NAME = 'IntelliCoder'
PACKAGE_NAME = 'intellicoder'


VERSION_PROMPT = (
    '{}\n\nCopyright 2015-2016 {} <rectigu@gmail.com>\n\n'
    'This is free software; see the source for '
    'copying conditions.\nThere is NO warranty; '
    'not even for MERCHANTABILITY nor \nFITNESS FOR '
    'A PARTICULAR PURPOSE.'.format(__version__, __author__)
)


getLogger(__name__).addHandler(NullHandler())

init(autoreset=True)

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
from logging import Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL
import os

from colorama import Fore, Style
from pkg_resources import resource_filename
try:
    from flufl.i18n import initialize
except ImportError:
    pass


__all__ = ['_', 'LevelFormatter']


try:
    os.environ['LOCPATH'] = resource_filename(__name__, 'share')
    _ = initialize('intellicoder')
except (KeyError, NameError):
    _ = lambda x: x


def green(text, **kwargs):
    return color(text, Fore.GREEN, **kwargs)


def yellow(text, **kwargs):
    return color(text, Fore.YELLOW, **kwargs)


def red(text, **kwargs):
    return color(text, Fore.RED, **kwargs)


def cyan(text, **kwargs):
    return color(text, Fore.CYAN, **kwargs)


def blue(text, **kwargs):
    return color(text, Fore.BLUE, **kwargs)


def color(text, fore='', back='', res=True):
    prefix = fore + Style.BRIGHT if fore else ''
    prefix += back if back else ''
    suffix = Style.RESET_ALL if res else ''
    return prefix + text + suffix


class LevelFormatter(Formatter):
    """
    Logging formatter.
    """
    critical_formatter = Formatter(red('critical: %(message)s'))
    error_formatter = Formatter(red('error: %(message)s'))
    warning_formatter = Formatter(yellow('warning: %(message)s'))
    info_formatter = Formatter(cyan('%(message)s'))
    debug_formatter = Formatter(
        green('debug: ') + blue('%(name)s.%(funcName)s: ') +
        green('%(message)s'))

    def __init__(self):
        Formatter.__init__(self)

    def format(self, record):
        """
        Format the record using the corresponding formatter.
        """
        if record.levelno == DEBUG:
            return self.debug_formatter.format(record)
        if record.levelno == INFO:
            return self.info_formatter.format(record)
        if record.levelno == ERROR:
            return self.error_formatter.format(record)
        if record.levelno == WARNING:
            return self.warning_formatter.format(record)
        if record.levelno == CRITICAL:
            return self.critical_formatter.format(record)

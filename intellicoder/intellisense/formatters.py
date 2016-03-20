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

from ..sources import make_c_args


logging = getLogger(__name__)


def with_formatter(formatter):
    """Apply a formatter function the return value
    of the decorated function.
    """
    def _decorator_after_args(unwrapped):
        def _wrapped(self, *args, **kwargs):
            logging.debug('unwrapped: %s', unwrapped)
            logging.debug('self: %s', self)
            logging.debug('args: %s', args)
            logging.debug('kwargs: %s', kwargs)
            return_value = unwrapped(self, *args, **kwargs)
            if 'raw' in kwargs and kwargs['raw']:
                return return_value
            else:
                return formatter(return_value)
        return _wrapped
    return _decorator_after_args


def format_module_funcs(raw):
    """Format the function names in a module."""
    return ' '.join(func[0] for func in raw)


def format_func(raw):
    """Format a string representing the function prototype."""
    if raw:
        return '{}\n{}({});\n'.format(
            raw[0], raw[1], make_c_args(raw[2])
        )
    return ''


def format_info(raw):
    """Format a string representing the information
    concerning the name.
    """
    sense = raw[1]
    new = '\n'.join(
        '{} {} {} {}{}'.format(
            i[0], sense.kind_id_to_name(i[1]),
            sense.file_id_to_name(i[2]).lower(),
            i[3] + ' ' if i[3] else '',
            i[4] if i[4] else '',
        ).strip()
        for i in raw[0]
    )
    return new


def format_names(raw):
    """Format a string representing the names contained in the files.
    """
    if raw:
        raw = [
            '{}:\n{}'.format(
                header.lower(), ' '.join(func[0] for func in funcs)
            )
            for header, funcs in raw
        ]
        return '\n'.join(raw)
    return ''


def format_kinds(raw):
    """Format a string representing the kinds."""
    return ' '.join('{} {}'.format(*kind) for kind in raw)


def format_comp(raw):
    """Format a struct or an union."""
    # TODO: Support structures or unions.
    print(raw)
    return 'TODO'

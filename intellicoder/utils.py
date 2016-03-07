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

from .i18n import _


logging = getLogger(__name__)


class AttrsGetter(object):
    """
    Get attributes from objects.
    """
    def __init__(self, objects, join=True):
        self.objects = objects
        self.join = join

    def __getattr__(self, name):
        """
        Get an attribute from multiple objects.
        """
        logging.debug(_('name: %s'), name)
        attrs = [getattr(one, name) for one in self.objects]
        if isinstance(attrs[0], str) and self.join:
            return ''.join(attrs)
        return attrs

    def get_attrs(self, *names):
        """
        Get multiple attributes from multiple objects.
        """
        attrs = [getattr(self, name) for name in names]
        return attrs

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
import re

from ..init import _
from ..utils import get_printable


logging = getLogger(__name__)


def sanitize_type(raw_type):
    """Sanitize the raw type string."""
    cleaned = get_printable(raw_type).strip()
    for bad in [
            r'__drv_aliasesMem', r'__drv_freesMem',
            r'__drv_strictTypeMatch\(\w+\)',
            r'__out_data_source\(\w+\)',
            r'_In_NLS_string_\(\w+\)',
            r'_Frees_ptr_', r'_Frees_ptr_opt_', r'opt_',
            r'\(Mem\) '
    ]:
        cleaned = re.sub(bad, '', cleaned).strip()
    if cleaned in ['_EXCEPTION_RECORD *', '_EXCEPTION_POINTERS *']:
        cleaned = cleaned.strip('_')
    cleaned = cleaned.replace('[]', '*')
    return cleaned


def clean_ret_type(ret_type):
    """Clean the erraneous parsed return type."""
    ret_type = get_printable(ret_type).strip()
    if ret_type == 'LRESULT LRESULT':
        ret_type = 'LRESULT'
    for bad in [
            'DECLSPEC_NORETURN', 'NTSYSCALLAPI', '__kernel_entry',
            '__analysis_noreturn', '_Post_equals_last_error_',
            '_Maybe_raises_SEH_exception_',
            '_CRT_STDIO_INLINE', '_ACRTIMP'
    ]:
        if bad in ret_type:
            ret_type = ret_type.replace(bad, '').strip()
            logging.debug(_('cleaned %s'), bad)
    return ret_type

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

from .converters import bytes_to_c_array


logging = getLogger(__name__)


# TODO: Use static templates, a.k.a, move out of Python code.
def make_init(body, use_hash):
    """
    Build source code for initialization.
    """
    include = '' if use_hash else '\n# include "string.h"\n'
    return """
# ifndef PREPROCESS
# include <stdint.h>

# include <windows.h>
# endif

# include "stdafx.h"
# include "defs.h"
# include "common.h"{}

# pragma code_seg(".pic")
# pragma data_seg(".pid")


windll_t _windll = {{ 0 }};


# ifndef _WIN64
uintptr_t get_reloc_delta(void)
{{
    uintptr_t reloc_delta;
  __asm {{
    call get_eip
    get_eip:
    mov ecx, dword ptr [esp]
    sub ecx, get_eip
    mov reloc_delta, ecx
  }}
  return reloc_delta;
}}
# endif


void init(void)
{{
{}
}}
""".strip().format(include, body) + '\n'


def make_c_header(name, front, body):
    """
    Build a C header from the front and body.
    """
    return """
{0}


# ifndef _GU_ZHENGXIONG_{1}_H
# define _GU_ZHENGXIONG_{1}_H


{2}


# endif /* {3}.h */
    """.strip().format(front, name.upper(), body, name) + '\n'


def make_windll(structs):
    """
    Build the windll structure.
    """
    name = 'windll_t'
    var = 'windll'
    struct_def = """
typedef struct _{0} {{
{1}
}}
{0};
""".strip().format(name, ''.join(structs))
    x86 = reloc_var(var, 'reloc_delta', True, name)
    x64 = '{0} *{1} = &_{1};\n'.format(name, var)
    return struct_def, x86, x64


def reloc_both(x86, x64):
    """
    Build relocation for x86 as well as x64.
    """
    if x86 or x64:
        return """
# ifdef _WIN64
{}
# else
uintptr_t reloc_delta = get_reloc_delta();
{}
# endif
""".strip().format(x64, x86) + '\n'
    return ''


def reloc_ptr(var_name, reloc_delta, var_type):
    """
    Build C source code to relocate a pointer variable.
    """
    return '{0}{1} = RELOC_PTR(_{1}, {2}, {0});\n'.format(
        var_type, var_name, reloc_delta
    )


def reloc_var(var_name, reloc_delta, pointer, var_type):
    """
    Build C source code to relocate a variable.
    """
    template = '{0} {3}{1} = RELOC_VAR(_{1}, {2}, {0});\n'
    return template.format(
        var_type, var_name, reloc_delta,
        '*' if pointer else ''
    )


def make_c_array_str(name, iterable):
    """
    Make a char array string in C.
    """
    return 'char {}[] = {{ {} }};\n'.format(
        name, bytes_to_c_array(iterable)
    )


def make_c_str(name, value):
    """
    Build a C string definition, which might be
    either a character array or character pointer.
    """
    return 'char PIS({}) = "{}";\n'.format(name, value)


def make_c_args(arg_pairs):
    """
    Build a C argument list from return type and arguments pairs.
    """
    logging.debug(arg_pairs)
    c_args = [
        '{} {}'.format(arg_type, arg_name) if arg_name else arg_type
        for dummy_number, arg_type, arg_name in sorted(arg_pairs)
    ]
    return ', '.join(c_args)


EXTERN_AND_SEG = """
# ifndef PREPROCESS
# include <windows.h>
# endif

# include "stdafx.h"
# include "defs.h"
# include "common.h"


extern windll_t _windll;

# pragma code_seg(".pic")
# pragma data_seg(".pid")
""".strip() + '\n\n'

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
from binascii import hexlify, unhexlify
import codecs

from more_itertools import chunked
from fn import _ as X

from .i18n import _
from .executables import Executable


logging = getLogger(__name__)


class Converter(object):
    """Binary converter."""
    cons_dict = {
        'sec': 'from_section'
    }
    func_dict = {
        'bin': 'to_bytes', 'hex': 'to_hex', 'esc': 'to_esc',
        'py': 'to_python', 'c': 'to_c', 'test': 'to_test'
    }

    @classmethod
    def uni_from(cls, source, *args, **kwargs):
        """Unified from."""
        logging.debug(_('source: %s, args: %s, kwargs: %s'),
                      source, args, kwargs)
        return getattr(cls, cls.cons_dict[source])(*args, **kwargs)

    def uni_to(self, target, *args, **kwargs):
        """Unified to."""
        logging.debug(_('target: %s, args: %s, kwargs: %s'),
                      target, args, kwargs)
        return getattr(self, self.func_dict[target])(*args, **kwargs)

    def __init__(self, stream, system='linux'):
        """stream: bytes."""
        self.stream = hexlify(stream).decode('utf-8')
        self.system = system

    @classmethod
    def from_section(cls, stream, section_name='.pic'):
        """Construct a Converter object from the specified section
        of the specified binary stream."""
        binary = Executable(stream)
        section_data = binary.get_section_data(section_name)
        return cls(section_data, binary.system)

    def to_test(self):
        """Convert to a complete testing C source code."""
        return make_test_shellcode(self.stream, self.system)

    def to_c(self):
        """Convert to a C variable."""
        return 'char shellcode[] = {}'.format(
            bytes_to_c_string(self.stream))

    # TODO
    def to_python(self):
        """Convert to a Python variable."""
        return 'shellcode = {}'.format(
            bytes_to_c_string(self.stream))

    def to_bytes(self):
        """Convert to bytes."""
        return unhexlify(self.stream.encode('utf-8'))

    def to_esc(self):
        """Convert to escape string."""
        chunks = chunked(self.stream, 2)
        return ''.join(r'\x' + ''.join(pair) for pair in chunks)

    def to_hex(self):
        """Convert to hexadecimal string."""
        return self.stream


def chunked_join(iterable, int1, int2, str1, str2, func):
    """Chunk and join."""
    chunks = list(chunked(iterable, int1))
    logging.debug(chunks)
    groups = [list(chunked(chunk, int2)) for chunk in chunks]
    logging.debug(groups)
    return str1.join([
        str2.join([func(''.join(chunk)) for chunk in chunks])
        for chunks in groups
    ])


def bytes_to_c_string(data):
    """
    Convert the hexadecimal string in to C-style string.
    """
    rows = chunked_join(data, 20, 2, '"\n    "', '', r'\x' + X)
    logging.debug(_('Returning rows: %s'), rows)
    return '"{}";'.format(rows)


def bytes_to_c_array(data):
    """
    Make a C array using the given string.
    """
    chars = [
        "'{}'".format(encode_escape(i))
        for i in decode_escape(data)
    ]
    return ', '.join(chars) + ', 0'


def decode_escape(orig):
    """Decode escape string."""
    decoder = codecs.getdecoder('unicode_escape')
    return decoder(orig)[0]


def encode_escape(orig):
    """Encode escape string."""
    encoder = codecs.getencoder('unicode_escape')
    return encoder(orig)[0].decode('utf-8')


def make_test_shellcode(data, system):
    """
    Construct C source code used for testing purposes
    from the C-style string represented shellcode.
    """
    logging.debug(_('Using data: %s'), data)
    logging.debug(_('Hexadecimal data: %s'), data)
    rows = bytes_to_c_string(data)
    if system == 'linux':
        include = """
# include <stdint.h>

# include <sys/mman.h>
"""
        protection = r"""
  int failure = mprotect((void *)((uintptr_t)shellcode & ~4095),
    4096, PROT_READ | PROT_WRITE | PROT_EXEC);

  if (failure) {
    printf ("mprotect\n");
    return EXIT_FAILURE;
  }

"""
    else:
        include = """

# include <windows.h>
"""
        protection = r"""
  DWORD why_must_this_variable;
  BOOL success = VirtualProtect(shellcode, COUNTOF(shellcode),
    PAGE_EXECUTE_READWRITE, &why_must_this_variable);

  if (!success) {
    printf ("VirtualProtect\n");
    return EXIT_FAILURE;
  }

"""
    source = r"""
/*
 * This file was generated by IntelliCoder, which is available at
 * https://github.com/NoviceLive/intellicoder.
 *
 * For those curious heads
 * striving to figure out what's under the hood.
 */


# include <stdlib.h>
# include <stdio.h>
{}

# define COUNTOF(a) (sizeof(a) / sizeof(a[0]))


int
main(void)
{{

  char shellcode[] = {};

  printf("5tr1eN(sH31lC0d3)=%d\n", COUNTOF(shellcode));

  {}

  ((void (*)(void))shellcode)();

  return EXIT_SUCCESS;
}}
""".strip().format(include.strip(), rows, protection.strip())
    return source + '\n'

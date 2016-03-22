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
import os
import sys
import string
import platform
from logging import getLogger
from itertools import chain, groupby
from subprocess import check_output, CalledProcessError
from operator import itemgetter
from glob import glob


from .init import _


logging = getLogger(__name__)


def get_printable(iterable):
    """
    Get printable characters from the specified string.
    Note that str.isprintable() is not available in Python 2.
    """
    if iterable:
        return ''.join(i for i in iterable if i in string.printable)
    return ''


def invert_dict(original):
    """
    Reverse a dictionary.
    """
    return {values: key for key, values in original.items()}


# TODO: Use plumbum.
def run_program(program, *args):
    """Wrap subprocess.check_output to make life easier."""
    real_args = [program]
    real_args.extend(args)
    logging.debug(_('check_output arguments: %s'), real_args)
    check_output(real_args, universal_newlines=True)


def read_file(filename):
    """Read a file."""
    logging.debug(_('Reading file: %s'), filename)
    try:
        with open(filename) as readable:
            return readable.read()
    except OSError:
        logging.error(_('Error reading file: %s'), filename)
        return ''


def get_parent_dir(name):
    """Get the parent directory of a filename."""
    parent_dir = os.path.dirname(os.path.dirname(name))
    if parent_dir:
        return parent_dir
    return os.path.abspath('.')


def glob_many(names):
    """Apply glob.glob to a list of filenames."""
    return list(chain.from_iterable([glob(name) for name in names]))


def is_64_bit():
    """Determine whether the system is 64-bit of not."""
    machine = platform.machine().lower()
    return machine in ['x86_64', 'amd64']


def is_windows():
    """Determine whether the system is Windows or not."""
    return sys.platform == 'win32'


def replace_ext(filename, ext, basename=True):
    """Replace the extension."""
    return split_ext(filename, basename)[0] + ext


def split_ext(path, basename=True):
    """Wrap them to make life easier."""
    if basename:
        path = os.path.basename(path)
    return os.path.splitext(path)


# TODO: Remove this probably.
def ad_hoc_magic_from_file(filename, **kwargs):
    """Ad-hoc emulation of magic.from_file from python-magic."""
    with open(filename, 'rb') as stream:
        head = stream.read(16)
        if head[:4] == b'\x7fELF':
            return b'application/x-executable'
        elif head[:2] == b'MZ':
            return b'application/x-dosexec'
        else:
            raise NotImplementedError()


def expand_path(*paths):
    """Expand the path with the directory of the executed file."""
    return os.path.join(
        os.path.dirname(os.path.realpath(sys.argv[0])), *paths)


def expand_user(*paths):
    """Wrap the os.path.expanduser to make life easier."""
    return os.path.expanduser(os.path.join('~', *paths))


def remove_false(iterable):
    """Remove False value from the iterable."""
    return filter(bool, iterable)


class AttrsGetter(object):
    """Get attributes from objects."""
    def __init__(self, objects, join=True):
        self.objects = objects
        self.join = join

    def __getattr__(self, name):
        """Get an attribute from multiple objects."""
        logging.debug(_('name: %s'), name)
        attrs = [getattr(one, name) for one in self.objects]
        if isinstance(attrs[0], str) and self.join:
            return ''.join(attrs)
        return attrs

    def get_attrs(self, *names):
        """Get multiple attributes from multiple objects."""
        attrs = [getattr(self, name) for name in names]
        return attrs


def get_dirs(top):
    """Get all directories in a directory recursively."""
    return [path[0] for path in os.walk(top)]


def translate_filenames(filenames):
    """Convert filenames from Linux to Windows."""
    if is_windows():
        return filenames
    for index, filename in enumerate(filenames):
        filenames[index] = vboxsf_to_windows(filename)


def vboxsf_to_windows(filename, letter='f:'):
    """Convert the Linux path name to a Windows one."""
    home = os.path.expanduser('~')
    filename = os.path.abspath(filename).replace(home, letter)
    return filename.replace('/', '\\')


def read_files(filenames, with_name=False):
    """Read many files."""
    text = [read_file(filename) for filename in filenames]
    if with_name:
        return dict(zip(filenames, text))
    return text


def write_files(text, where='.'):
    """Write many files."""
    for filename in text:
        target = os.path.join(where, filename)
        write_file(target, text[filename])


def write_file(filename, text):
    """Write text to a file."""
    logging.debug(_('Writing file: %s'), filename)
    try:
        with open(filename, 'w') as writable:
            writable.write(text)
    except (PermissionError, NotADirectoryError):
        logging.error(_('Error writing file: %s'), filename)
        return False
    return True


def stylify_files(text):
    """Stylify many files."""
    for filename in text:
        text[filename] = stylify_code(text[filename])
    return text


def stylify_code(code):
    """Stylify the C source code using astyle."""
    try:
        output = check_output(
            ['astyle', '--max-code-length=69', '--indent=spaces=2'],
            universal_newlines=True, input=code
        )
    except (OSError, CalledProcessError, TypeError):
        logging.debug(_('failed to stylify code'))
        return code
    return output


def sort_values(dictionary, reverse=False):
    """Sort a dictionary by its values."""
    return sort_item(dictionary.items(), 1, reverse)


def sort_item(iterable, number, reverse=False):
    """Sort the itertable according to the given number item."""
    return sorted(iterable, key=itemgetter(number), reverse=reverse)


def print_if(value):
    """Print when the argument is not False."""
    if value:
        print(value)


def hash_func(name):
    """Hash the string using a hash algorithm found in
    tombkeeper/Shellcode_Template_in_C.
    """
    ret = 0
    for i in name:
        ret = ((ret << 5) + ret + ord(i)) & 0xffffffff
    return hex(ret)


def remove_many(original, many):
    """Remove a list of items from the original list."""
    for one in many:
        if one in original:
            original.remove(one)


def remove_dups(iterable):
    """Remove duplicated items in the iterable."""
    return sorted(set(iterable))


def remove_by(keys, original):
    """Remove items in a list according to another list."""
    for i in [
            original[index]
            for index, needed in enumerate(keys) if not needed
    ]:
        original.remove(i)


def group_by(iterable, key_func):
    """Wrap itertools.groupby to make life easier."""
    groups = (
        list(sub) for key, sub in groupby(iterable, key_func)
    )
    return zip(groups, groups)


def ends_with_punctuation(iterable):
    """Determine whether a string ends with a punctuation or not."""
    return iterable[-1] in string.punctuation

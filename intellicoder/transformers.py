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
from functools import partial

from .init import _
from .sources import (
    make_c_array_str, make_c_str, reloc_ptr, reloc_var, reloc_both,
    EXTERN_AND_SEG
)
from .utils import remove_dups, sort_values


logging = getLogger(__name__)


class Transformer(object):
    """Source code transformation."""
    FUNC_NAME_RE = r'[_\w][_\w\d]*(?=\s*\()'
    # No Good: r'(?<=").+?(?=")'
    STR_LITERAL_RE = r'".+?"'
    FUNC_NAME_PREFIX = 'ic_func_'
    STR_VAR_PREFIX = 'ic_str_'
    str_table = {}
    func_table = {}

    def __init__(self, database):
        self.database = database

    def transform_sources(self, sources):
        for filename in sources:
            logging.info(_('Processing file: %s'), filename)
            updated = update_func_body(
                sources[filename], self.replace_source)
            sources[filename] = self._post_update(updated)
        sources.update(self._build_funcs())
        return sources

    def replace_source(self, body, name):
        logging.debug(_('Processing function body: %s'), name)
        replaced = re.sub(
            self.FUNC_NAME_RE, self._func_replacer, body)
        replaced = re.sub(
            self.STR_LITERAL_RE, self._string_replacer, replaced)
        return self._build_strings() + replaced
        return replaced


class WindowsTransformer(object):
    """Windows Transformer."""
    C_KEYWORDS = ['if', 'switch', 'while', 'for']

    BLACKLIST = C_KEYWORDS + [
        'main', 'comment', 'code_seg', 'data_seg'
    ]

    def __init__(self, database):
        self.database = database

    def transform_sources(self, sources, with_string=False):
        """Get the defintions of needed strings and functions
        after replacement.
        """
        modules = {}
        updater = partial(
            self.replace_source, modules=modules, prefix='string_')
        for filename in sources:
            updated = update_func_body(sources[filename], updater)
            sources[filename] = EXTERN_AND_SEG + updated
        logging.debug('modules: %s', modules)
        return sources, self.build_funcs(modules)

    def replace_source(self, source, name, modules, prefix):
        """Scan C source code for string literals as well as
        function calls and do replacement using the specified
        replacing function.
        Note that the regular expression currently used for strings
        is naive or quick and dirty.
        """
        needs_windll = False

        def _func_replacer(match, modules, windll):
            matched = match.group(0)
            if matched in self.BLACKLIST:
                return matched
            module = self.database.query_func_module(matched)
            if module:
                try:
                    modules[module[0]] += [module[1]]
                except KeyError:
                    modules[module[0]] = [module[1]]
                if windll:
                    return '{}->{}.{}'.format(windll, *module)
                return '{}->{}'.format(*module)
            return matched

        replacer = partial(
            _func_replacer, modules=modules, windll='windll')
        replaced = re.sub(r'[_\w][_\w\d]*(?=\s*\()',
                          replacer, source)

        if source != replaced:
            needs_windll = True

        str_table = {}

        def _string_replacer(match):
            matched = match.group()[1:-1]
            try:
                number = str_table[matched]
            except KeyError:
                number = len(str_table) + 1
                str_table.update({matched: number})
            return '{}{}'.format(prefix, number)

        replaced = re.sub(r'".+?"', _string_replacer, replaced)
        strings, relocs = self.build_strings(str_table, prefix)
        strings = ''.join(strings).strip()
        windll32 = reloc_var('windll', 'reloc_delta', True,
                             'windll_t')
        if needs_windll:
            relocs += [windll32]
        if strings:
            strings = '\n' + strings
            if not needs_windll:
                relocs += [windll32]
                needs_windll = True
        windll64 = ''
        if needs_windll:
            windll64 = '{0} *{1} = &_{1};\n'.format('windll_t',
                                                    'windll')
        relocs = reloc_both(''.join(relocs), windll64)
        if name in ['main']:
            replaced = '\ninit();' + replaced
        return strings + relocs + replaced

    @staticmethod
    def build_funcs(modules):
        """Build a used functions and modules list
        for later consumption.
        """
        kernel32 = ['kernel32_']
        try:
            kernel32 += remove_dups(modules['kernel32'])
        except KeyError:
            if len(modules) and 'LoadLibraryA' not in kernel32:
                kernel32.insert(1, 'LoadLibraryA')
        if len(modules) > 1 and 'LoadLibraryA' not in kernel32:
            kernel32.insert(1, 'LoadLibraryA')
        if 'GetProcAddress' not in kernel32:
            kernel32.insert(1, 'GetProcAddress')
        logging.debug('kernel32: %s', kernel32)
        for module, funcs in modules.items():
            logging.debug('%s: %s', module, funcs)
            if module != 'kernel32':
                kernel32.extend([module + '_'] + remove_dups(funcs))
        return kernel32

    @staticmethod
    def build_strings(strings, prefix):
        """Construct string definitions according to
        the previously maintained table.
        """
        strings = [
            (
                make_c_str(prefix + str(number), value),
                reloc_ptr(
                    prefix + str(number), 'reloc_delta', 'char *'
                )
            ) for value, number in sort_values(strings)
        ]
        return [i[0] for i in strings], [i[1] for i in strings]


class LinuxTransformer(Transformer):
    """
    Linux Transformer.
    """
    main_foremost = """\
# ifndef DECLARE
# define DECLARE
# endif /* DECLARE */

# include "syscall.h"
# include "syscall.c"


int ATTR
main(void);
\n
"""
    source_foremost = """\
# ifdef DECLARE
# undef DECLARE
# endif /* DECLARE */

# include "syscall.h"
\n
"""

    def _func_replacer(self, match):
        matched = match.group(0)
        logging.debug(_('Processing function name: %s'), matched)
        items = self.database.query_decl(name=matched)
        if items:
            item = items[0]
            logging.debug(_('item: %s'), item)
            self.func_table.update({item.name: item})
            return self.FUNC_NAME_PREFIX + matched
        else:
            logging.warning(_('Function not handled: %s'), matched)
            return matched

    def _string_replacer(self, match):
        matched = match.group()[1:-1]
        logging.debug(_('Processing string literal: %s'), matched)
        try:
            number = self.str_table[matched]
        except KeyError:
            number = len(self.str_table) + 1
            self.str_table.update({matched: number})
        return self.STR_VAR_PREFIX + str(number)

    def _post_update(self, updated):
        return self.main_foremost + updated

    def _build_strings(self):
        logging.debug(_('Using str_table: %s'), self.str_table)
        strings = []
        for value, number in sort_values(self.str_table):
            var_name = self.STR_VAR_PREFIX + str(number)
            strings.append(make_c_array_str(var_name, value))
        return '  ' + '  '.join(strings)

    def _build_funcs(self):
        logging.debug(_('Using func_table: %s'), self.func_table)
        funcs = []
        for name in sorted(self.func_table):
            one = self.func_table[name]
            if one.argc == 0:
                decl = 'syscall{}(long, {})'.format(
                    one.argc, one.name)
            else:
                decl = 'syscall{}(long, {}, {})'.format(
                    one.argc, one.name,
                    one.args.replace('__user ', '').replace(
                        'umode_t', 'mode_t'))
            funcs.append(decl)
        return {'syscall.c': self.source_foremost + '\n'.join(funcs)}


def update_func_body(original, updater=None):
    """Update all function body using the updating function."""
    updated = ''
    regex = r'([_\w][_\w\d]*)\s*\(.*\)\s*\{'
    match = re.search(regex, original)
    while match:
        name = match.group(1)
        logging.debug(_('Found candidate: %s'), name)
        start = match.end()
        end = start + find_balance_index(original[start:])
        body = original[start:end]
        if updater:
            body = updater(body, name)
        updated += original[:start] + '\n' + body + original[end]
        original = original[end + 1:]
        match = re.search(regex, original)
    return updated


def find_balance_index(source, start='{', end='}'):
    """Get the first balance index."""
    state = 1
    for index, char in enumerate(source):
        if char == start:
            state += 1
        elif char == end:
            state -= 1
        if state == 0:
            return index
    raise RuntimeError('This should not happen: Balance Not Found')

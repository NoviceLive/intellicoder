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
import string
from collections import namedtuple
from configparser import ConfigParser

from .sources import (
    make_c_args, make_c_str, reloc_ptr, reloc_var,
    make_c_header, make_init, reloc_both, make_windll
)
from .utils import (
    AttrsGetter, expand_user, group_by, hash_func,
    ends_with_punctuation, stylify_files
)
from .init import _


logging = getLogger(__name__)


class Synthesizer(object):
    """Synthesizer."""
    def __init__(self, database):
        self.database = database
        self.generic = True
        filename = expand_user('.intellicoder', 'code.conf')
        logging.debug(_('Reading configuration file: %s'), filename)
        conf = ConfigParser()
        conf.read(filename)
        print(conf['code']['base'])

    def synthesize(self, modules, use_string, x64, native):
        """Transform sources."""
        # code_opts = CodeOpts(
        #     str.lower, None if use_string else hash_func,
        #     'reloc_delta', '->',
        #     True)
        # gen_opts = GenOpts('defs', transformed)
        print(hash_func)
        groups = group_by(modules, ends_with_punctuation)
        sources = self.make_source(groups, self.database)
        if sources:
            return stylify_files(
                {'defs.h': sources[0], 'init.c': sources[1]}
            )
        else:
            return ''

    def make_source(self, groups, code_opts, gen_opts):
        """Build the final source code for all modules."""
        modules = self.make_modules(groups, code_opts)
        var_decls = modules.var_decls
        relocs = AttrsGetter(modules.relocs)
        x86, x64 = relocs.get_attrs('x86', 'x64')
        if code_opts.windll:
            structs, x86_reloc, x64_reloc = make_windll(
                modules.structs
            )
            x86 += x86_reloc
            x64 += x64_reloc
        else:
            structs = ''.join(modules.structs)
        c_relocs = reloc_both(relocs.strings + x86, x64)
        data = var_decls.strip()
        c_header = make_c_header(
            gen_opts.filename, 'NOTICE',
            modules.typedefs + structs + data
        )
        c_source = make_init(
            modules.hashes + c_relocs + modules.libprocs,
            callable(code_opts.hash_func)
        )
        return [c_header, c_source]

    def make_modules(self, groups, code_opts):
        """Build shellcoding files for the module."""
        modules = []
        for raw_module, raw_funcs in groups:
            module = raw_module[0].strip().strip(string.punctuation)
            funcs = [func.strip() for func in raw_funcs]
            args = [self.database.query_args(func, raw=True)
                    for func in funcs]
            if self.generic:
                args = [arg if arg else ('VOID *', [])
                        for arg in args]
            else:
                args = [arg for arg in args if arg]
            if not args:
                logging.info(_('%s not found.'), module)
                continue
            logging.debug(module)
            module = ModuleSource(module, zip(funcs, args),
                                  code_opts)
            modules.append(module.c_source())
        return AttrsGetter(modules)


class ModuleSource(object):
    """Represent a module with its functions and code options."""
    def __init__(self, name, funcs=None, opts=None):
        self.name = name.lower()
        if funcs is None:
            self.funcs = []
        else:
            self.funcs = list(funcs)
        if opts is None:
            self.opts = DEFAULT_CODE_OPTS
        else:
            self.opts = opts
        if callable(self.opts.hash_func):
            for i in self.funcs:
                if i[0] == 'GetProcAddress':
                    self.funcs.remove(i)
                    break

    def c_source(self):
        """Return strings."""
        relocs = Relocs(
            ''.join(self.c_self_relocs()), *self.c_module_relocs()
        )
        return Source(
            ''.join(self.c_typedefs()),
            '' if self.opts.no_structs else self.c_struct(),
            ''.join(self.c_hashes()),
            ''.join(self.c_var_decls()),
            relocs,
            self.c_loadlib() + ''.join(self.c_getprocs())
        )

    def c_typedefs(self):
        """Get the typedefs of the module."""
        defs = []
        attrs = self.opts.attrs + '\n' if self.opts.attrs else ''
        for name, args in self.funcs:
            logging.debug('name: %s args: %s', name, args)
            defs.append(
                'typedef\n{}\n{}{}({});\n'.format(
                    args[0], attrs,
                    self._c_type_name(name), make_c_args(args[2])
                )
            )
        return defs

    def c_struct(self):
        """Get the struct of the module."""
        member = '\n'.join(self.c_member_funcs(True))
        if self.opts.windll:
            return 'struct {{\n{}{} }} {};\n'.format(
                self._c_dll_base(), member, self.name
            )
        return 'typedef\nstruct {2} {{\n{0}\n{1}}}\n{3};\n'.format(
            self._c_dll_base(), member, *self._c_struct_names()
        )

    def c_hashes(self):
        """Get the hashes of the module including functions and DLLs.
        """
        if callable(self.opts.hash_func):
            hashes = [
                '# define {}{} {}\n'.format(
                    self.opts.prefix, name, self.opts.hash_func(name)
                ) for name, dummy_args in self.funcs
            ]
        else:
            hashes = [
                make_c_str(self.opts.prefix + name, name)
                for name, dummy_args in self.funcs
            ]
        if self.name != 'kernel32':
            hashes = [
                make_c_str(self.opts.prefix + self.name, self.name)
            ] + hashes
        return hashes

    def c_self_relocs(self):
        """Build relocation for strings."""
        relocs = []
        if not callable(self.opts.hash_func):
            relocs = [
                reloc_ptr(
                    self.opts.prefix + name, self.opts.reloc_delta,
                    'char *'
                )
                for name, dummy_args in self.funcs
            ]
        if self.name != 'kernel32':
            relocs = [
                reloc_ptr(
                    self.opts.prefix + self.name,
                    self.opts.reloc_delta, 'char *'
                )
            ] + relocs
        return relocs

    def c_var_decls(self):
        """Get the needed variable definitions."""
        if self.opts.no_structs:
            mod_decl = 'HMODULE {} = NULL;\n'.format(self.name)
            return [mod_decl] + [
                '{} *{} = NULL;\n'.format(
                    self._c_type_name(name), name
                )
                for name, dummy_args in self.funcs
            ]
        if self.opts.windll:
            return ''
        return [
            '{} _{} = {{ 0 }};\n'.format(
                self._c_struct_names()[1], self.name
            )
        ]

    def c_module_relocs(self):
        """Build relocation for the module variable."""
        if self.opts.no_structs or self.opts.windll:
            return '', ''
        x86 = reloc_var(
            self.name, self._c_struct_names()[1],
            self.opts.reloc_delta,
            self._c_uses_pointer()
        )
        x64 = '{0} *{1} = &_{1};\n'.format(
            self._c_struct_names()[1], self.name
        ) if self._c_uses_pointer() else ''
        return x86, x64

    def c_loadlib(self):
        """Get the loadlib of the module."""
        name = self._c_base_var()
        kernel32 = 'windll->kernel32.'
        if self.name == 'kernel32':
            loadlib = '{} = get_kernel32_base();\n'.format(
                'kernel32' if self.opts.no_structs
                else kernel32 + self.opts.base
            )
        else:
            loadlib = '{} = {}LoadLibraryA({}{});\n'.format(
                name,
                '' if self.opts.no_structs else kernel32,
                self.opts.prefix, self.name
            )
        return loadlib + self._c_null_check(name)

    def c_getprocs(self):
        """Get the getprocs of the module."""
        getprocs = []
        for name, dummy_args in self.funcs:
            if name == 'GetProcAddress':
                if callable(self.opts.hash_func):
                    continue
                getter = 'get_proc_by_string'
            elif self.opts.no_structs:
                getter = 'GetProcAddress'
            else:
                getter = 'windll->kernel32.GetProcAddress'
            if callable(self.opts.hash_func):
                getter = 'get_proc_by_hash'
            if self.opts.no_structs:
                var = name
            else:
                var = 'windll->{}.{}'.format(self.name, name)
            getproc = '{} = ({} *){}({}, {}{});\n'.format(
                var,
                self._c_type_name(name),
                getter,
                self._c_base_var(),
                self.opts.prefix, name
            )
            getprocs.append(getproc + self._c_null_check(var))
        return getprocs

    def c_member_funcs(self, for_struct=False):
        """Get the decls of the module."""
        decls = [
            '{} *{};'.format(self._c_type_name(name), name)
            for name, dummy_args in self.funcs
        ]
        if for_struct:
            return decls
        return [self._c_mod_decl()] + decls

    def _c_struct_names(self):
        """Return two names for use with typedef."""
        return '_{}_t'.format(self.name), self.name + '_t'

    def _c_dll_base(self):
        """Return a C declaration of a DllBase."""
        return 'HMODULE {};'.format(self.opts.base)

    def _c_mod_decl(self):
        """Return the C declaration for the module base."""
        return 'HMODULE {} = NULL;'.format(self.name)

    def _c_null_check(self, name):
        """Return the C source code checking NULL for the name."""
        if self.opts.no_checks:
            return ''
        return """
if (!{}) {{
  return;
}}
            """.strip().format(name) + '\n'

    def _c_type_name(self, name):
        """Return the function type name."""
        return self.opts.modifier(name) + '_t'

    def _c_uses_pointer(self):
        """Determine whether we are using pointers or not."""
        return self.opts.member_accessor == '->'

    def _c_base_var(self):
        """Return the name of the module base variable."""
        if self.opts.no_structs:
            return self.name
        return 'windll->{}.{}'.format(
            self.name, self.opts.base
        )


CodeOpts = namedtuple(
    'CodeOpts',
    [
        'modifier', 'hash_func', 'no_structs', 'no_checks',
        'attrs', 'prefix', 'base', 'reloc_delta', 'member_accessor',
        'windll'
    ]
)


Source = namedtuple(
    'Source',
    [
        'typedefs', 'structs', 'hashes',
        'var_decls', 'relocs', 'libprocs'
    ]
)


Relocs = namedtuple(
    'Relocs',
    ['strings', 'x86', 'x64']
)


GenOpts = namedtuple(
    'GenOpts',
    [
        'filename', 'main_source'
    ]
)


DEFAULT_CODE_OPTS = CodeOpts(
    modifier=str.lower, hash_func=None,
    no_structs=False, no_checks=False,
    attrs='WINAPI', prefix='hash_', base='DllBase',
    reloc_delta='reloc_delta', member_accessor='->', windll=True
)

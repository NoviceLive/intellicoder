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
import sys
import os
import logging
from collections import OrderedDict

import click

from . import VERSION_PROMPT, PROGRAM_NAME
from .init import _, LevelFormatter
from .converters import Converter
from .database import Database
from .intellisense.database import SenseWithExport
from .transformers import WindowsTransformer, LinuxTransformer
from .builders import LinuxBuilder
from .synthesizers import Synthesizer
from .utils import (
    expand_path, is_windows, write_file, read_files, write_files,
    stylify_code, stylify_files, get_parent_dir, print_if, split_ext,
    vboxsf_to_windows)


@click.group(
    context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(VERSION_PROMPT,
                      '-V', '--version', prog_name=PROGRAM_NAME)
@click.option('-v', '--verbose', count=True, help='Be verbose.')
@click.option('-q', '--quiet', count=True, help='Be quiet.')
@click.option('-d', '--database', type=click.Path(),
              default=expand_path('data', 'default.db'),
              help='Connect the database.')
@click.option('-s', '--sense', type=click.Path(),
              default=expand_path('ignored', 'default.db'),
              help='Connect the IntelliSense database.')
@click.pass_context
def cli(context, verbose, quiet, database, sense):
    """Position Independent Programming For Humans."""
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(LevelFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING + (quiet-verbose)*10)
    logging.debug(_('Subcommand: %s'), context.invoked_subcommand)
    context.obj['database'] = Database(database)
    context.obj['sense'] = SenseWithExport(sense).__enter__()


@cli.command()
@click.argument('filenames', nargs=-1, required=True)
@click.option('-u', '--uri', help='Connect the RPC server.')
@click.option('-c', '--cl-args', help='Pass arguments to cl.exe.')
@click.option('-l', '--link-args',
              help='Pass to arguments link.exe.')
@click.option('-6', '--x64', is_flag=True, help='Use x64.')
@click.option('-n', '--native', is_flag=True, help='Use native.')
def build(filenames, uri, cl_args, link_args, x64, native):
    """Build (Don't use for the time being).
    """
    logging.info(_('This is source file building mode.'))
    logging.debug(_('filenames: %s'), filenames)
    logging.debug(_('uri: %s'), uri)
    logging.debug(_('cl_args: %s'), cl_args)
    logging.debug(_('link_args: %s'), link_args)
    logging.debug(_('native: %s'), native)
    logging.debug(_('x64: %s'), x64)

    if is_windows():
        pass
        # ret = msbuild(uri, native, list(filenames), x64=x64,
        #               cl_args=cl_args, link_args=link_args)
    else:
        builder = LinuxBuilder()
        ret = builder.build(filenames, x64, 'src', 'out')
    sys.exit(ret)


@cli.command()
@click.argument('filenames', nargs=-1, required=True,
                type=click.Path(exists=True))
@click.option('-6', '--x64', is_flag=True)
@click.pass_context
def linux(context, filenames, x64):
    """Linux (Don't use for the time being).
    """
    src = 'src'
    bits = '64' if x64 else '32'
    binary = 'sc' + bits
    source = bits + '.c'
    database = context.obj['database']
    sources = read_files(filenames, with_name=True)
    transformer = LinuxTransformer(database)
    updated = transformer.transform_sources(sources)

    os.makedirs(src, exist_ok=True)
    write_files(updated, where=src)
    builder = LinuxBuilder()
    logging.info(_('Building transformed sources'))
    builder.build(filenames, x64, 'src', binary)
    logging.info(_('Dumpping compiled binary'))
    logging.debug(_('Binary: %s Source: %s'), binary, source)
    # with open(binary, 'rb') as stream, \
    #      open(source, 'w') as test:
    #     logging.debug(_('transferring control to dump'))
    #     context.invoke(dump, streams=[stream], output=test)
    # logging.info(_('Building dumpped source'))
    # builder.build([source], x64, '', bits)


@cli.command()
@click.argument('filenames', type=click.Path(exists=True),
                nargs=-1, required=True)
@click.option('-s', '--with-string', is_flag=True)
@click.option('-6', '--x64', is_flag=True)
@click.option('-n', '--native', is_flag=True)
@click.option('-O', '--no-outputs', is_flag=True)
@click.option('-m', '--make', is_flag=True)
@click.option('-u', '--uri', help='Connect the RPC server.')
@click.pass_context
def tr(context, filenames, uri, with_string, native, x64,
              make, no_outputs):
    """Transform (Don't use for the time being).
    """
    logging.info(_('Entering transformation mode'))
    src = 'src'
    sense = context.obj['sense']
    sources = read_files(filenames, with_name=True)

    transformed, modules = WindowsTransformer(
        sense).transform_sources(sources, with_string)
    if no_outputs:
        print('\n\n'.join(transformed.values()))
    else:
        if not os.path.exists(src):
            os.makedirs(src)
        write_files(stylify_files(transformed), where=src)

    synthesized = Synthesizer(sense).synthesize(
        modules, with_string, x64, native
    )
    if no_outputs:
        print('\n\n'.join(synthesized.values()))
    # else:
    #     if not os.path.exists(src):
    #         os.makedirs(src)
    #     write_files(stylify_files(synthesized), where=src)

    # if not make:
    #     return
    # shellcode = make_shellcode(filenames, with_string, x64, native)
    # if not shellcode:
    #     return 1
    # shellcode = stylify_code(shellcode)
    # if no_outputs:
    #     print(shellcode)
    # else:
    #     parent_dir = get_parent_dir(filenames[0])
    #     out_dir = os.path.join(parent_dir, 'bin')
    #     if not os.path.exists(out_dir):
    #         os.makedirs(out_dir)
    #     test_name = '64.c' if x64 else '32.c'
    #     test_name = os.path.join(parent_dir, test_name)
    #     out_name = '64.exe' if x64 else '32.exe'
    #     out_name = os.path.join(out_dir, out_name)
    #     out_name = vboxsf_to_windows(out_name)
    #     out_dir = vboxsf_to_windows(out_dir)
    #     if write_file(test_name, shellcode):
    #         link_args = ['/debug', '/out:' + out_name]
    #         if msbuild(uri, [vboxsf_to_windows(test_name)],
    #                    [], link_args, x64, out_dir):
    #             print(_('Happy Hacking'))
    #         else:
    #             logging.error(_('failed to compile shellcode'))
    sys.exit(0)


@cli.command()
@click.argument('keywords', nargs=-1)
@click.option('-m', '--module', is_flag=True)
@click.option('-r', '--raw', is_flag=True)
@click.option('-k', '--kind', default=None)
@click.pass_context
def search(context, keywords, module, raw, kind):
    """Query Windows identifiers and locations.

    Windows database must be prepared before using this.
    """
    logging.info(_('Entering search mode'))
    sense = context.obj['sense']
    func = sense.query_names if module else sense.query_info
    none = True
    for keyword in keywords:
        output = func(keyword, raw, kind)
        if output:
            none = False
            print(output)
        else:
            logging.warning(_('No results: %s'), keyword)
    sys.exit(1 if none else 0)


@cli.command()
@click.argument('names', nargs=-1)
@click.pass_context
def winapi(context, names):
    """Query Win32 API declarations.

    Windows database must be prepared before using this.
    """
    logging.info(_('Entering winapi mode'))
    sense = context.obj['sense']
    none = True
    for name in names:
        code = sense.query_args(name)
        if code:
            none = False
            print(stylify_code(code))
        else:
            logging.warning(_('Function not found: %s'), name)
    sys.exit(1 if none else 0)


@cli.command()
@click.argument('keywords', nargs=-1)
@click.pass_context
def kinds(context, keywords):
    """Operate on IntelliSense kind ids and names.

    Without an argument, list all available kinds and their ids.

    Windows database must be prepared before using this.
    """
    logging.info(_('Entering kind mode'))
    logging.debug('keywords: %s', keywords)
    sense = context.obj['sense']
    print(sense.query_kinds(keywords))
    sys.exit(0)


@cli.command()
@click.argument('keywords', nargs=-1)
@click.option('-m', '--module', is_flag=True)
@click.option('-u', '--update', is_flag=True)
@click.pass_context
def export(context, keywords, module, update):
    """Operate on libraries and exported functions.

    Windows database must be prepared before using this.
    """
    logging.info(_('Entering export mode'))
    sense = context.obj['sense']
    if update:
        exports = OrderedDict()
        from .executables.pe import PE
        for filename in keywords:
            module = split_ext(filename, basename=True)[0]
            with open(filename, 'rb') as stream:
                exports.update(
                    {module: PE(stream).get_export_table()})
        sense.make_export(exports)
        none = True
    else:
        if module:
            func = sense.query_module_funcs
        else:
            func = sense.query_func_module
        none = True
        for keyword in keywords:
            output = func(keyword)
            if output:
                none = False
                print(output)
            else:
                logging.warning(_('No results: %s'), keyword)
    sys.exit(1 if none else 0)


@cli.command()
@click.argument('filenames', nargs=-1, required=True,
                type=click.File())
@click.pass_context
def add(context, filenames):
    """Add data on Linux system calls.

    Arguments shall be *.tbl files from Linux x86 source code,
    or output from grep.

    Delete the old database before adding if necessary.
    """
    logging.info(_('Current Mode: Add Linux data'))
    context.obj['database'].add_data(filenames)
    sys.exit(0)


@cli.command()
@click.argument('filenames', nargs=-1, required=True)
@click.option('-6', '--x64', is_flag=True)
@click.option('-c', '--cl-args')
@click.option('-l', '--link-args')
@click.option('-o', '--output')
def make(filenames, x64, cl_args, link_args, output):
    """Make binaries from sources.

    Note that this is incomplete.
    """
    from .msbuild import Builder
    builder = Builder()
    builder.build(list(filenames), x64=x64,
                  cl_args=cl_args, link_args=link_args,
                  out_dir=output)


@cli.command()
@click.argument('keywords', nargs=-1, required=True)
@click.option('-3', '--x86', is_flag=True)
@click.option('-6', '--x64', is_flag=True)
@click.option('-c', '--common', is_flag=True)
@click.option('-x', '--x32', is_flag=True)
@click.pass_context
def info(context, keywords, x86, x64, x32, common):
    """Find in the Linux system calls.
    """
    logging.info(_('Current Mode: Find in Linux'))
    database = context.obj['database']
    for one in keywords:
        abis = ['i386', 'x64', 'common', 'x32']
        if x86:
            abis = ['i386']
        if x64:
            abis = ['x64', 'common']
        if x32:
            abis = ['x32', 'common']
        if common:
            abis = ['common']
        items = database.query_item(one, abis)
        if not items:
            logging.warning(_('Item not found: %s %s'), one, abis)
            continue
        for item in items:
            print(item.name, item.abi, item.number)
            decl = database.query_decl(name=item.name)
            if not decl:
                logging.warning(_('Decl not found: %s'), item.name)
                continue
            for one in decl:
                print(one.decl(), '/* {} */'.format(one.filename))
    sys.exit(0)


@cli.command()
@click.argument('arg')
@click.option('-f', '--from', 'source', default='sec',
              type=click.Choice(Converter.cons_dict.keys()),
              help='Convert from this form.')
@click.option('-t', '--to', 'target', default='test',
              type=click.Choice(Converter.func_dict.keys()),
              help='Convert to this form.')
@click.option('-o', '--output', 'filename',
              help='Write to a file (print to stdout by default).')
@click.option('-j', '--section', default='.pic', show_default=True,
              help='Use this section.')
def conv(arg, source, target, filename, section):
    """Convert binary.

    Extract bytes in the given section from binary files
    and construct C source code
    that can be used to test as shellcode.

    Supported executable formats:
    ELF via pyelftools and PE via pefile.
    """
    logging.info(_('This is binary conversion mode.'))
    section = section.encode('utf-8')
    if source == 'sec':
        arg = open(arg, 'rb')
    if source == 'sec':
        kwargs = dict(section_name=section)
    else:
        kwargs = dict()
    result = Converter.uni_from(source, arg, **kwargs).uni_to(target)
    if result:
        if filename:
            logging.info(
                _('Writing shellcode to the file: %s'), filename)
            mode = 'wb' if target == 'bin' else 'w'
            with open(filename, mode) as output:
                output.write(result)
        else:
            print(result)
    else:
        logging.error(_('Failed.'))
    if source == 'sec':
        arg.close()
    return 0


def main():
    """Start hacking the world."""
    cli(obj={})

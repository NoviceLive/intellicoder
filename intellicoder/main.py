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
import logging

import click

from . import VERSION_PROMPT, PROGRAM_NAME
from .i18n import _
from .converters import Converter


@click.group(
    context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(VERSION_PROMPT,
                      '-V', '--version', prog_name=PROGRAM_NAME)
@click.option('-v', '--verbose', count=True, help='Be verbose.')
@click.option('-q', '--quiet', count=True, help='Be quiet.')
@click.pass_context
def cli(context, verbose, quiet):
    """
    IntelliCoder.
    """
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(LevelFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING + (quiet-verbose)*10)
    logging.debug(_('Invoked Subcommand: %s'),
                  context.invoked_subcommand)


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
    """
    Convert binary.

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
            mode = 'wb' if to == 'bin' else 'w'
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
    """
    Start hacking the world.
    """
    cli(obj={})


class LevelFormatter(logging.Formatter):
    """
    Logging formatter.
    """
    from colorama import Fore, Style

    critical_formatter = logging.Formatter(
        Fore.RED + Style.BRIGHT + 'critical: %(message)s')
    error_formatter = logging.Formatter(
        Fore.MAGENTA + Style.BRIGHT + 'error: %(message)s')
    warning_formatter = logging.Formatter(
        Fore.YELLOW + Style.BRIGHT + 'warning: %(message)s')
    info_formatter = logging.Formatter(
        Fore.CYAN + Style.BRIGHT + '%(message)s')
    debug_formatter = logging.Formatter(
        Fore.GREEN + Style.BRIGHT + 'debug: ' +
        Fore.BLUE + '%(name)s.%(funcName)s: ' +
        Fore.GREEN + Style.BRIGHT + '%(message)s')

    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record):
        """
        Format the record using the corresponding formatter.
        """
        if record.levelno == logging.DEBUG:
            return self.debug_formatter.format(record)
        if record.levelno == logging.INFO:
            return self.info_formatter.format(record)
        if record.levelno == logging.ERROR:
            return self.error_formatter.format(record)
        if record.levelno == logging.WARNING:
            return self.warning_formatter.format(record)
        if record.levelno == logging.CRITICAL:
            return self.critical_formatter.format(record)

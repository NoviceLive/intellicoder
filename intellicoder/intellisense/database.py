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
import sqlite3 # TODO: Use an ORM.
from os.path import splitext

try:
    import adodbapi
except ImportError:
    pass

from ..init import _
from ..utils import invert_dict
from .sanitizers import sanitize_type, clean_ret_type
from .formatters import (
    with_formatter, format_info, format_func, format_kinds,
    format_names, format_comp, format_module_funcs
)


logging = getLogger(__name__)


class IntelliSense(object):
    """Represent the IntelliSense with concentration
    upon its database.
    """
    def __init__(self, database):
        self.database = database
        self.con = None
        self.cursor = None
        self._kind_name_to_id = None
        self._kind_id_to_name = None

    # TODO: Remove this.
    def __enter__(self):
        """Establish database connection."""
        if splitext(self.database)[1] == '.sdf':
            # TODO: Support SQL Server Compact via adodbapi.
            conn_str = 'provider=microsoft.sqlserver.ce.oledb.4.0;' \
                       'data source={};'.format(self.database)
            logging.debug(_('adodbapi connection: %s'), conn_str)
            try:
                self.con = adodbapi.connect(conn_str)
            except NameError:
                raise
        else:
            logging.debug(_('sqlite connection: %s'), self.database)
            self.con = sqlite3.connect(self.database)
        self.cursor = self.con.cursor()
        self._init_kind_converter()
        return self

    def __exit__(self, *dummy):
        """Close database connection."""
        logging.debug(_('closing connection...'))
        self.con.close()

    @with_formatter(format_func)
    def query_args(self, name):
        """Query the return type and argument list of the specified
        function in the specified database.
        """
        sql = 'select type, id from code_items ' \
              'where kind = 22 and name = ?'
        logging.debug('%s %s', sql, (name,))
        self.cursor.execute(sql, (name,))
        func = self.cursor.fetchone()
        if func:
            sql = 'select param_number, type, name ' \
                  'from code_items where parent_id = ?'
            logging.debug('%s %s', sql, (func[1],))
            self.cursor.execute(sql, (func[1],))
            args = self.cursor.fetchall()
            ret_type = clean_ret_type(func[0])
            args = [
                (arg_number, sanitize_type(arg_type), arg_name)
                for arg_number, arg_type, arg_name in args
            ]
            return ret_type, name, args
        return None

    @with_formatter(format_info)
    def query_info(self, name, like, kind):
        """Query the information of the name in the database."""
        kind = self._make_kind_id(kind)
        # Database from VS2015 does not have assoc_text.
        #
        # sql = 'select name, kind, file_id, type, assoc_text ' \
        #       'from code_items ' \
        #       'where name {} ?'.format('like' if like else '=')
        sql = 'select name, kind, file_id, type ' \
              'from code_items ' \
              'where name {} ?'.format('like' if like else '=')
        args = (name,)
        if like:
            sql += ' escape ?'
            args = (name, '\\')
        if kind:
            sql += ' and kind = ?'
            args = (name, kind)
        if like and kind:
            args = (name, '\\', kind)
        logging.debug('%s %s', sql, args)
        self.cursor.execute(sql, args)
        return self.cursor.fetchall(), self

    @with_formatter(format_names)
    def query_names(self, name, like, kind):
        """
        Query function declarations in the files.
        """
        kind = self._make_kind_id(kind)
        sql = 'select id, name from files ' \
              'where leaf_name {} ?'.format('like' if like else '=')
        args = (name,)
        if like:
            sql += ' escape ?'
            args = (name, '\\')
        logging.debug('%s %s', sql, args)
        self.cursor.execute(sql, args)
        ids = self.cursor.fetchall()
        files = []
        for file_id, header in ids:
            sql = 'select name from code_items ' \
                  'where file_id = ?'
            args = (file_id,)
            if kind:
                sql += 'and kind = ?'
                args = (file_id, kind)
            logging.debug('%s %s', sql, args)
            self.cursor.execute(sql, args)
            files.append((header, self.cursor.fetchall()))
        return files

    @with_formatter(format_comp)
    def query_struct(self, name):
        """Query struct."""
        sql = 'select id, file_id, name from code_items '\
              'where name = ?'
        self.cursor.execute(sql, (name,))
        for i in self.cursor.fetchall():
            sql = 'select id, type, name from code_items ' \
                  'where parent_id = ?'
            self.cursor.execute(sql, (i[0],))
            members = self.cursor.fetchall()
            if members:
                print(self.file_id_to_name(i[1]), i[2])
                print(members)

    @with_formatter(format_kinds)
    def query_kinds(self, raw_kinds):
        """Query kinds."""
        kinds = []
        for kind in raw_kinds:
            logging.debug(_('querying %s'), kind)
            if kind.isdigit():
                kind_name = self.kind_id_to_name(int(kind))
                if kind_name:
                    kinds.append((kind, kind_name))
                else:
                    logging.warning(_('id not found: %s'), kind)
            else:
                kind_id = self.kind_name_to_id(kind)
                if kind_id:
                    kinds.append((kind_id, kind))
                else:
                    logging.warning(_('name not found: %s'), kind)
        return kinds if kinds else self._kind_id_to_name.items()

    def file_id_to_name(self, file_id):
        """Convert a file id to the file name."""
        sql = 'select name from files where id = ?'
        logging.debug('%s %s', sql, (file_id,))
        self.cursor.execute(sql, (file_id,))
        name = self.cursor.fetchone()
        if name:
            return name[0]
        return ''

    def _make_kind_id(self, name_or_id):
        """Make kind_id from kind_name or kind_id."""
        if not name_or_id:
            return None
        if name_or_id.isdigit():
            return name_or_id
        return self.kind_name_to_id(name_or_id)

    def kind_id_to_name(self, kind_id):
        """Convert a kind id to the kind name."""
        return self._kind_id_to_name.get(kind_id)

    def kind_name_to_id(self, kind_name):
        """Convert a kind name to the kind id."""
        return self._kind_name_to_id.get(kind_name)

    def _init_kind_converter(self):
        """Make a dictionary mapping kind ids to the names."""
        sql = 'select id, name, parser from code_item_kinds'
        logging.debug(sql)
        self.cursor.execute(sql)
        kinds = self.cursor.fetchall()
        self._kind_id_to_name = {i[0]: i[1] for i in kinds}
        self._kind_name_to_id = invert_dict(self._kind_id_to_name)


class SenseWithExport(IntelliSense):
    """Represent the IntelliSense database with
    library exported functions.
    """
    def make_export(self, exports):
        """Populate library exported function data."""
        sql = 'drop table if exists export'
        logging.debug(sql)
        self.cursor.execute(sql)
        sql = 'create table if not exists export ' \
              '(func text unique, module text)'
        logging.debug(sql)
        self.cursor.execute(sql)
        for module in exports:
            logging.debug(_('insering exports from %s'), module)
            sql = 'insert into export values (?, ?)'
            for func in exports[module]:
                if func:
                    try:
                        self.cursor.execute(sql, (func, module))
                    except sqlite3.IntegrityError:
                        pass
        self.con.commit()

    def query_func_module(self, func):
        """Query the module name of the specified function."""
        sql = 'select module from export where func = ?'
        logging.debug('%s %s', sql, (func,))
        try:
            self.cursor.execute(sql, (func,))
        except sqlite3.OperationalError:
            logging.error(
                _('Have you fully prepared Windows database?'))
            return None
        module = self.cursor.fetchone()
        if module:
            return (module[0], func)
        logging.debug(_('function not found: %s'), func)
        afunc = func + 'A'
        logging.debug('%s %s', sql, (afunc,))
        self.cursor.execute(sql, (afunc,))
        module = self.cursor.fetchone()
        if module:
            logging.warning(_('using ANSI version: %s'), afunc)
            return (module[0], afunc)
        logging.warning(_('Not handled: %s or %s'), func, afunc)
        return None

    @with_formatter(format_module_funcs)
    def query_module_funcs(self, module):
        """Query the functions in the specified module."""
        sql = 'select func from export where module = ?'
        logging.debug('%s %s', sql, (module,))
        try:
            self.cursor.execute(sql, (module,))
        except sqlite3.OperationalError:
            logging.error(
                _('Have you fully prepared Windows database?'))
            return None
        funcs = self.cursor.fetchall()
        return funcs

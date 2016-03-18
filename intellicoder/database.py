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
import re

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from more_itertools import chunked

from .i18n import _
from .utils import remove_false


logging = getLogger(__name__)

Base = declarative_base()
Session = sessionmaker()


class Database(object):
    def __init__(self, filename):
        self.filename = filename
        self.engine = create_engine('sqlite:///{}'.format(filename))
        Base.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session()

    def query_item(self, key, abis):
        try:
            key = int(key)
            field = 'number'
        except ValueError:
            try:
                key = int(key, 16)
                field = 'number'
            except ValueError:
                field = 'name'
        arg = and_(getattr(Item, field) == key,
                   or_(Item.abi == abi for abi in abis))
        return self.session.query(Item).filter(arg).all()

    def query_decl(self, **kwargs):
        return self.session.query(Decl).filter_by(**kwargs).all()

    def add_data(self, filenames):
        def _parse_table(table):
            def _parse_line(line):
                return line.split('\t')
            lines = (
                _parse_line(one) for one in table.splitlines()
                if re.match(r'^\d', one)
            )
            return (remove_false(one) for one in lines)

        def _parse_decl(decl):
            index = len('SYSCALL_DEFINE')
            argc = decl[index]
            rest = decl[index + 1:][1:-1].split(',')
            name = rest[0]
            # args = [one.strip() for one in rest[1:]]
            args = ','.join(rest[1:])
            return name, argc, args

        def _parse_line(line):
            index = line.find(':')
            if index == -1:
                raise RuntimeError('This is unexpected: %s', line)
            filename = line[:index]
            decl = line[index + 1:]
            return filename, _parse_decl(decl)

        def _split_into_lines(grep_output):
            lines = grep_output.replace('\n\n', '\n')
            lines = lines.replace('\n\t', '').replace('\t', ' ')
            return lines.strip().splitlines()

        for one in filenames:
            if one.name.endswith('.tbl'):
                for item in _parse_table(one.read()):
                    args = list(item)
                    if len(args) != 5:
                        args += [''] * (5 - len(args))
                    self.session.add(
                        Item(name=args[2], abi=args[1],
                             number=args[0], entry=args[3],
                             compat=args[4]))
            else:
                for line in _split_into_lines(one.read()):
                    filename, rest = (_parse_line(line))
                    self.session.add(
                        Decl(name=rest[0], filename=filename,
                             argc=rest[1], args=rest[2]))
        self.session.commit()


class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    abi = Column(String)
    number = Column(Integer)
    entry = Column(String)
    compat = Column(String)

    def __repr__(self):
        template = '<Item(item_id={0.item_id}, name={0.name}' \
                   ', abi={0.abi}, number={0.number}' \
                   ', entry={0.entry}, compat={0.compat})>'
        return template.format(self)


class Decl(Base):
    __tablename__ = 'decls'
    decl_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    filename = Column(String)
    argc = Column(Integer)
    args = Column(String)

    def decl(self):
        logging.debug(_('args: %s'), self.args)
        args = self.args.strip().replace('__user ', '').split(',')
        logging.debug(_('args: %s'), args)
        args = [''.join(pair) for pair in chunked(args, 2)]
        return 'long {}({});'.format(
            self.name.strip(), ', '.join(args))

    def __repr__(self):
        template = '<Decl(name={0.name}, filename={0.filename}' \
                   ', argc={0.argc}, args={0.args})>'
        return template.format(self)

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

from setuptools import setup, find_packages


__author__ = 'Gu Zhengxiong'
__version__ = '0.5.0'


PROGRAM_NAME = 'IntelliCoder'
PACKAGE_NAME = PROGRAM_NAME.lower()


my_dir = dirname(argv[0])
version_file = 'version.txt'
version_path = join(my_dir, PACKAGE_NAME, version_file)
with open(version_path) as stream:
    __version__ = stream.read().strip()

with open(join(my_dir, 'requirements.txt')) as stream:
    requirements = stream.read().splitlines()


setup(
    name=PROGRAM_NAME,
    version=__version__,
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ic={}.main:main'.format(PACKAGE_NAME)
        ]
    },
    author=__author__,
    author_email='rectigu@gmail.com',
    description='Shellcoder',
    license='GPL',
    keywords='Shellcoder',
    url='https://github.com/NoviceLive/{}'.format(PACKAGE_NAME),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)

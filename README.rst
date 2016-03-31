IntelliCoder
============

Position independent programming for humans.

Or seriously, automation of position independent code generation
from normal C source code.

Current State: It's a pretotype or a toy
serving educational purposes.


.. image:: https://travis-ci.org/NoviceLive/intellicoder.svg?branch=master
    :target: https://travis-ci.org/NoviceLive/intellicoder


Installation
============

Clone and run.

- ``git clone --depth 1 https://github.com/NoviceLive/intellicoder.git``
- ``pip install -r requirements.txt``
- ``./ic.py --help``


Usable Features
===============


Usage
-----

See ``./ic.py --help``.

Note that some commands are not usable and
some may change without notification.

::

   ./ic.py --help
   Usage: ic.py [OPTIONS] COMMAND [ARGS]...

     Position Independent Programming For Humans.

   Options:
     -V, --version        Show the version and exit.
     -v, --verbose        Be verbose.
     -q, --quiet          Be quiet.
     -d, --database PATH  Connect the database.
     -s, --sense PATH     Connect the IntelliSense database.
     -h, --help           Show this message and exit.

   Commands:
     add     Add data on Linux system calls.
     build   Build (Don't use for the time being).
     conv    Convert binary.
     export  Operate on libraries and exported functions.
     info    Find in the Linux system calls.
     kinds   Operate on IntelliSense kind ids and names.
     lin     Linux.
     make    Make binaries from sources.
     search  Query Windows identifiers and locations.
     win     Windows.
     winapi  Query Win32 API declarations.


Shellcode Extraction & Conversion
---------------------------------

See ``./ic.py conv --help``.


Linux System Call Searching
---------------------------

See ``./ic.py info --help``.


Examples
++++++++

::

   $ ./ic.py info fork
   fork i386 2
   long fork(); /* kernel/fork.c */
   fork common 57
   long fork(); /* kernel/fork.c */

   $ ./ic.py info 11
   execve i386 11
   long execve(const char * filename,  const char *const * argv,  const char *const * envp); /* fs/exec.c */
   long execve(const char * filename, const compat_uptr_t * argv, const compat_uptr_t * envp); /* fs/exec.c */
   munmap common 11
   long munmap(unsigned long addr,  size_t len); /* mm/nommu.c */
   long munmap(unsigned long addr,  size_t len); /* mm/mmap.c */

   $ ./ic.py info 0xb
   execve i386 11
   long execve(const char * filename,  const char *const * argv,  const char *const * envp); /* fs/exec.c */
   long execve(const char * filename, const compat_uptr_t * argv, const compat_uptr_t * envp); /* fs/exec.c */
   munmap common 11
   long munmap(unsigned long addr,  size_t len); /* mm/nommu.c */
   long munmap(unsigned long addr,  size_t len); /* mm/mmap.c */


Directory Structure
===================

intellicoder/
-------------

intellicoder/executables/
+++++++++++++++++++++++++

A simple abstraction layer of binary executables
based on existing predominant libraries such as pyelftools_.

Note that it's incomplete and ad-hoc for the time being.

intellicoder/msbuild/
+++++++++++++++++++++

Despite its name, ``intellicoder.msbuild`` does not wrap MSBuild_.

Instead, it wraps against MSVC_ with SDKs_ (and WDKs_) to ease
the automation of compilation on Windows.

intellicoder/intellisense/
++++++++++++++++++++++++++

Collect necessary information, e.g., function prototypes,
leveraging the database of IntelliSense_.


static/
-------

C library sources and headers.

These are licensed under `GNU Lesser General Public License`_.


recipes/
--------

Examples.

Note thta some are work in progress and may not work as intended.


Copying Conditions
==================

Unless otherwise specified, IntelliCoder is licensed under
`GNU General Public License`_.


.. _pyelftools: https://github.com/eliben/pyelftools
.. _MSBuild: https://msdn.microsoft.com/en-us/library/0k6kkbsd.aspx
.. _MSVC: https://msdn.microsoft.com/en-us/library/hh875057.aspx
.. _SDKs: https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk
.. _WDKs: https://msdn.microsoft.com/en-us/library/windows/hardware/ff557573%28v=vs.85%29.aspx
.. _IntelliSense: https://msdn.microsoft.com/en-us/library/hcw1s69b.aspx
.. _GNU Lesser General Public License: http://www.gnu.org/licenses/lgpl.html
.. _GNU General Public License: http://www.gnu.org/licenses/gpl.html

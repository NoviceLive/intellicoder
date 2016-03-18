IntelliCoder
============


Current State: Work in progress and **incomplete**.


.. image:: https://travis-ci.org/NoviceLive/intellicoder.svg?branch=master
    :target: https://travis-ci.org/NoviceLive/intellicoder


Installation
============

Clone and run.

- ``git clone --depth 1 https://github.com/NoviceLive/intellicoder.git``
- ``pip install -r requirements.txt``
- ``pip install -r requirements3.txt``
- ``./ic.py --help``


Current Features
================


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

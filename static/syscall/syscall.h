/*
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
*/

# ifndef _GU_ZHENGXIONG_SYSCALL_H
# define _GU_ZHENGXIONG_SYSCALL_H


# ifndef CPP
# include <sys/syscall.h>
# include <sys/types.h>
# include <sys/stat.h>
# endif /* CPP */


# define _CONCAT(one, two) one##two
# define CONCAT(one, two) _CONCAT(one, two)


# define ATTR __attribute__ ((section(".pic")))
# define PREFIX ic_func_
# define INPUT0 "a" // eax / rax.


# ifdef __i386__

# define SYSCALL "int $0x80"
# define INPUT1 "b"
# define INPUT2 "c"
# define INPUT3 "d"
# define INPUT4 "S"
# define INPUT5 "D"
# define INPUT6 "" // ebp.

# endif /* __i386__ */


# ifdef __amd64__

# define SYSCALL "syscall"
# define INPUT1 "D"
# define INPUT2 "S"
# define INPUT3 "d"
# define INPUT4 "" // r10.
# define INPUT5 "" // r8.
# define INPUT6 "" // r9.

# endif /*  __amd64__ */


# ifdef DECLARE

# define syscall0(type, name)                   \
  type ATTR CONCAT(PREFIX, name)(void);

# define syscall1(type, name, type1, arg1)          \
  type ATTR CONCAT(PREFIX, name)(type1 arg1);

# define syscall2(type, name, type1, arg1, type2, arg2)         \
  type ATTR CONCAT(PREFIX, name)(type1 arg1, type2 arg2);

# define syscall3(type, name, type1, arg1, type2, arg2,     \
                  type3, arg3)                              \
  type ATTR CONCAT(PREFIX, name)(type1 arg1, type2 arg2,  \
                                 type3 arg3);
# else /* DECLARE */

# define syscall0(type, name)                   \
  type ATTR CONCAT(PREFIX, name)(void)    \
  {                                             \
    long result;                                \
    __asm__ volatile (SYSCALL                   \
                      : "=a" (result)           \
                      : INPUT0 (SYS_##name));   \
    return result;                              \
  }

# define syscall1(type, name, type1, arg1)          \
  type ATTR CONCAT(PREFIX, name)(type1 arg1)  \
  {                                                 \
    long result;                                    \
    __asm__ volatile (SYSCALL                       \
                      : "=a" (result)               \
                      : INPUT0 (SYS_##name),        \
                        INPUT1 ((long)arg1));       \
    return result;                                  \
  }

# define syscall2(type, name, type1, arg1, type2, arg2)         \
  type ATTR CONCAT(PREFIX, name)(type1 arg1, type2 arg2)  \
  {                                                             \
    long result;                                                \
    __asm__ volatile (SYSCALL                                   \
                      : "=a" (result)                           \
                      : INPUT0 (SYS_##name),                    \
                        INPUT1 ((long)arg1),                    \
                        INPUT2 ((long)arg2));                   \
    return result;                                              \
  }

# define syscall3(type, name, type1, arg1, type2, arg2,     \
                  type3, arg3)                              \
  type ATTR CONCAT(PREFIX, name)(type1 arg1, type2 arg2,  \
                                   type3 arg3)          \
  {                                                         \
    long result;                                            \
    __asm__ volatile (SYSCALL                               \
                      : "=a" (result)                       \
                      : INPUT0 (SYS_##name),                \
                        INPUT1 ((long)arg1),                \
                        INPUT2 ((long)arg2),                \
                        INPUT3 ((long)arg3));               \
    return result;                                          \
  }

# endif /* DECLARE */


# endif /* syscall.h */

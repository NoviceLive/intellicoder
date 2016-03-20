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

from .converters import bytes_to_c_array


logging = getLogger(__name__)


# TODO: Use static templates, a.k.a, move out of Python code.
def make_init(body, use_hash):
    """
    Build source code for initialization.
    """
    include = '' if use_hash else '\n# include "string.h"\n'
    return """
# ifndef PREPROCESS
# include <stdint.h>

# include <windows.h>
# endif

# include "stdafx.h"
# include "defs.h"
# include "common.h"{}

# pragma code_seg(".pic")
# pragma data_seg(".pid")


windll_t _windll = {{ 0 }};


# ifndef _WIN64
uintptr_t get_reloc_delta(void)
{{
    uintptr_t reloc_delta;
  __asm {{
    call get_eip
    get_eip:
    mov ecx, dword ptr [esp]
    sub ecx, get_eip
    mov reloc_delta, ecx
  }}
  return reloc_delta;
}}
# endif


void init(void)
{{
{}
}}
""".strip().format(include, body) + '\n'


def make_c_header(name, front, body):
    """
    Build a C header from the front and body.
    """
    return """
{0}


# ifndef _GU_ZHENGXIONG_{1}_H
# define _GU_ZHENGXIONG_{1}_H


{2}


# endif /* {3}.h */
    """.strip().format(front, name.upper(), body, name) + '\n'


def make_windll(structs):
    """
    Build the windll structure.
    """
    name = 'windll_t'
    var = 'windll'
    struct_def = """
typedef struct _{0} {{
{1}
}}
{0};
""".strip().format(name, ''.join(structs))
    x86 = reloc_var(var, 'reloc_delta', True, name)
    x64 = '{0} *{1} = &_{1};\n'.format(name, var)
    return struct_def, x86, x64


def reloc_both(x86, x64):
    """
    Build relocation for x86 as well as x64.
    """
    if x86 or x64:
        return """
# ifdef _WIN64
{}
# else
uintptr_t reloc_delta = get_reloc_delta();
{}
# endif
""".strip().format(x64, x86) + '\n'
    return ''


def reloc_ptr(var_name, reloc_delta, var_type):
    """
    Build C source code to relocate a pointer variable.
    """
    return '{0}{1} = RELOC_PTR(_{1}, {2}, {0});\n'.format(
        var_type, var_name, reloc_delta
    )


def reloc_var(var_name, reloc_delta, pointer, var_type):
    """
    Build C source code to relocate a variable.
    """
    template = '{0} {3}{1} = RELOC_VAR(_{1}, {2}, {0});\n'
    return template.format(
        var_type, var_name, reloc_delta,
        '*' if pointer else ''
    )


def make_c_array_str(name, iterable):
    """
    Make a char array string in C.
    """
    return 'char {}[] = {{ {} }};\n'.format(
        name, bytes_to_c_array(iterable)
    )


def make_c_str(name, value):
    """
    Build a C string definition, which might be
    either a character array or character pointer.
    """
    return 'char PIS({}) = "{}";\n'.format(name, value)


def make_c_args(arg_pairs):
    """
    Build a C argument list from return type and arguments pairs.
    """
    logging.debug(arg_pairs)
    c_args = [
        '{} {}'.format(arg_type, arg_name) if arg_name else arg_type
        for dummy_number, arg_type, arg_name in sorted(arg_pairs)
    ]
    return ', '.join(c_args)


EXTERN_AND_SEG = """
# ifndef PREPROCESS
# include <windows.h>
# endif

# include "stdafx.h"
# include "defs.h"
# include "common.h"


extern windll_t _windll;

# pragma code_seg(".pic")
# pragma data_seg(".pid")
""".strip() + '\n\n'


COMMON_FILES = {
    'common.h': """
/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 */


# ifndef _GU_ZHENGXIONG_COMMON_H
# define _GU_ZHENGXIONG_COMMON_H


# ifndef PREPROCESS
# include <stdint.h>

# include <windows.h>
# endif
# include "structs.h"


# ifdef _WIN64
# define get_current_peb() ((PEB *)__readgsqword(0x60))
# define PIV(name) name
# define PIS(name) name##[]
# else
# define get_current_peb() ((PEB *)__readfsdword(0x30))
# define PIV(name) _##name
# define PIS(name) * _##name

# define RELOC_CONST(var_name, reloc_delta) \
  ((var_name) + (reloc_delta))

# define RADDR(var_name, reloc_delta) \
  ((uintptr_t)&(var_name) + (reloc_delta))

# define RELOC_PTR(var_name, delta, var_type) \
  (var_type) \
  (*(uintptr_t *)((uintptr_t)&(var_name) + (0)) + (delta))

# define RELOC_VAR(var_name, reloc_delta, var_type) \
  (var_type *)RADDR(var_name, reloc_delta)
# endif


FARPROC
get_proc_by_hash(HMODULE base, uint32_t proc_hash);


__forceinline
HMODULE
get_kernel32_base(void)
{
  PEB *peb = NULL;
  PEB_LDR_DATA *ldr = NULL;
  LIST_ENTRY list = { 0 };
  LDR_DATA_TABLE_ENTRY *entry = NULL;
  HMODULE kernel32 = NULL;

  peb = get_current_peb();
  ldr = peb->Ldr;
  list = ldr->InInitializationOrderModuleList;

  entry =
    CONTAINING_RECORD(list.Flink,
                      LDR_DATA_TABLE_ENTRY,
                      InInitializationOrderLinks);
  while (entry->BaseDllName.Buffer[6] != '3') {
    entry =
      CONTAINING_RECORD(entry->InInitializationOrderLinks.Flink,
                        LDR_DATA_TABLE_ENTRY,
                        InInitializationOrderLinks);
  }
  kernel32 = entry->DllBase;

  return kernel32;
}


# endif /* common.h */
""".strip(),
    'structs.h': """
/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 */


# ifndef _GU_ZHENGXIONG_STRUCTS_H
# define _GU_ZHENGXIONG_STRUCTS_H

# ifndef PREPROCESS
# include <windows.h>
# endif


typedef
struct _UNICODE_STRING {
  USHORT Length;
  USHORT MaximumLength;
  USHORT *Buffer;
}
UNICODE_STRING, *PUNICODE_STRING;


typedef
struct _LDR_DATA_TABLE_ENTRY {
  LIST_ENTRY InLoadOrderLinks;
  LIST_ENTRY InMemoryOrderLinks;
  LIST_ENTRY InInitializationOrderLinks;
  VOID *DllBase;
  VOID *EntryPoint;
  ULONG SizeOfImage;
  UNICODE_STRING FullDllName;
  UNICODE_STRING BaseDllName;
  /* We don't need them. */
}
LDR_DATA_TABLE_ENTRY, *PLDR_DATA_TABLE_ENTRY;


typedef
struct _PEB_LDR_DATA {
  ULONG Length;
  UCHAR Initialized;
  VOID *SsHandle;
  LIST_ENTRY InLoadOrderModuleList;
  LIST_ENTRY InMemoryOrderModuleList;
  LIST_ENTRY InInitializationOrderModuleList;
  VOID *EntryInProgress;
  UCHAR ShutdownInProgress;
  VOID *ShutdownThreadId;
}
PEB_LDR_DATA, *PPEB_LDR_DATA;


typedef
struct _PEB {
  UCHAR InheritedAddressSpace;
  UCHAR ReadImageFileExecOptions;
  UCHAR BeingDebugged;
  union {
    UCHAR BitField;
    struct {
      UCHAR ImageUsesLargePages: 1;
      UCHAR IsProtectedProcess: 1;
      UCHAR IsLegacyProcess: 1;
      UCHAR IsImageDynamicallyRelocated: 1;
      UCHAR SkipPatchingUser32Forwarders: 1;
      UCHAR SpareBits: 3;
    };
  };
  VOID *Mutant;
  VOID *ImageBaseAddress;
  PEB_LDR_DATA *Ldr;
  /* We don't need them. */
}
PEB, *PPEB;


# endif /* structs.h */
""".strip()
}


HASH_FILE = {
    'hash.c': """
# ifndef PREPROCESS
# include <stdint.h>

# include <windows.h>
# endif

# include "structs.h"

# pragma code_seg(".pic")


__forceinline
uint32_t hash_func(char *string)
{
  uint32_t ret = 0;
  while (*string)
    ret = (ret << 5) + ret + *string++;
  return ret;
}


FARPROC
get_proc_by_hash(HMODULE base, uint32_t proc_hash)
{
  IMAGE_NT_HEADERS *nt_headers = NULL;
  IMAGE_EXPORT_DIRECTORY *export_directory = NULL;
  DWORD *name_table = NULL;
  int i = 0;
  WORD ordinal = 0;
  DWORD address = 0;

  nt_headers = (IMAGE_NT_HEADERS *)
    ((uintptr_t)base + ((IMAGE_DOS_HEADER *)base)->e_lfanew);
  export_directory = (IMAGE_EXPORT_DIRECTORY *)
    ((uintptr_t)base +
     nt_headers->OptionalHeader.DataDirectory[0].VirtualAddress);
  name_table = (DWORD *)
    ((uintptr_t)base + export_directory->AddressOfNames);
  for (i = 0; i < export_directory->NumberOfNames; ++i) {
    char *name = (char *)((uintptr_t)base + name_table[i]);
    if (hash_func(name) == proc_hash) {
# ifdef DEBUG
      __debugbreak();
# endif
      ordinal = ((WORD *)
                 ((uintptr_t)base +
                  export_directory->AddressOfNameOrdinals))[i];
      address = ((DWORD *)
                 ((uintptr_t)base +
                  export_directory->AddressOfFunctions))[ordinal];
      return (FARPROC)((uintptr_t)base + address);
    }
  }
  return NULL;
}
""".strip()
}


STRING_FILE = {
    'string.h': """
# ifndef _GU_ZHENGXIONG_STRING_H
# define _GU_ZHENGXIONG_STRING_H


__forceinline
FARPROC
get_proc_by_string(HMODULE base, char *proc_string)
{
  IMAGE_NT_HEADERS *nt_headers = NULL;
  IMAGE_EXPORT_DIRECTORY *export_directory = NULL;
  DWORD *name_table = NULL;
  int i = 0;
  WORD ordinal = 0;
  DWORD address = 0;

  nt_headers = (IMAGE_NT_HEADERS *)
    ((uintptr_t)base + ((IMAGE_DOS_HEADER *)base)->e_lfanew);
  export_directory = (IMAGE_EXPORT_DIRECTORY *)
    ((uintptr_t)base +
     nt_headers->OptionalHeader.DataDirectory[0].VirtualAddress);
  name_table = (DWORD *)
    ((uintptr_t)base + export_directory->AddressOfNames);
  for (i = 0; i < export_directory->NumberOfNames; ++i) {
    char *name = (char *)((uintptr_t)base + name_table[i]);
    if (strcmp(name, proc_string) == 0) {
# ifdef DEBUG
      __debugbreak();
# endif
      ordinal = ((WORD *)
                 ((uintptr_t)base +
                  export_directory->AddressOfNameOrdinals))[i];
      address = ((DWORD *)
                 ((uintptr_t)base +
                  export_directory->AddressOfFunctions))[ordinal];
      return (FARPROC)((uintptr_t)base + address);
    }
  }
  return NULL;
}


# endif /* string.h */
""".strip()
}

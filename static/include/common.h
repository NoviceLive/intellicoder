/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 *
 * LGPL.
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

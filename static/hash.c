/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 *
 * Licensed under GNU Lesser General Public License.
 * See COPYING.LIB.txt.
 */


# ifndef CPP
# include <stdint.h>

# include <windows.h>
# endif /* CPP */

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


/* No ``__forceinline`` here
 * because we are going to use it many times.
 */
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

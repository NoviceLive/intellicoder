/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 *
 * Licensed under GNU Lesser General Public License.
 * See COPYING.LIB.txt.
 */


# ifndef _GU_ZHENGXIONG_STRING_H
# define _GU_ZHENGXIONG_STRING_H


/* ``__forceinline`` here
 * because we will use it only once.
 */
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
    /* Use /Oi for inlined intrinsic function ``strcmp``.
     * See ``Intrinsics Available on All Architectures``,
     * https://msdn.microsoft.com/en-us/library/5704bbxw.aspx, and
     * ``/Oi (Generate Intrinsic Functions)``,
     * https://msdn.microsoft.com/en-us/library/f99tchzc.aspx,
     * for more information.
     */
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

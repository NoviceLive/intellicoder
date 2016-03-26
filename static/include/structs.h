/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 *
 * LGPL.
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

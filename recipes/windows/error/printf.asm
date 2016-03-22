00000000`001bf550 48895c2408      mov     qword ptr [rsp+8],rbx
00000000`001bf555 57              push    rdi
00000000`001bf556 4883ec60        sub     rsp,60h
00000000`001bf55a 0f10055f020000  movups  xmm0,xmmword ptr [00000000`001bf7c0]
00000000`001bf561 488b0550020000  mov     rax,qword ptr [00000000`001bf7b8]
00000000`001bf568 0f100d61020000  movups  xmm1,xmmword ptr [00000000`001bf7d0]
00000000`001bf56f 4889442478      mov     qword ptr [rsp+78h],rax
00000000`001bf574 8a0576020000    mov     al,byte ptr [00000000`001bf7f0]
00000000`001bf57a 488bf9          mov     rdi,rcx
00000000`001bf57d 88442450        mov     byte ptr [rsp+50h],al
00000000`001bf581 0f11442420      movups  xmmword ptr [rsp+20h],xmm0
00000000`001bf586 0f100553020000  movups  xmm0,xmmword ptr [00000000`001bf7e0]
00000000`001bf58d 0f114c2430      movups  xmmword ptr [rsp+30h],xmm1
00000000`001bf592 0f11442440      movups  xmmword ptr [rsp+40h],xmm0
00000000`001bf597 ff158b020000    call    qword ptr [00000000`001bf828]
00000000`001bf59d 8bc8            mov     ecx,eax
00000000`001bf59f e86cffffff      call    00000000`001bf510
00000000`001bf5a4 488bd8          mov     rbx,rax
00000000`001bf5a7 4885c0          test    rax,rax
00000000`001bf5aa 7427            je      00000000`001bf5d3
00000000`001bf5ac 488d4c2478      lea     rcx,[rsp+78h]
00000000`001bf5b1 4c8bc0          mov     r8,rax
00000000`001bf5b4 488bd7          mov     rdx,rdi
00000000`001bf5b7 ff158b020000    call    qword ptr [00000000`001bf848]
00000000`001bf5bd ff156d020000    call    qword ptr [00000000`001bf830]
00000000`001bf5c3 4c8bc3          mov     r8,rbx
00000000`001bf5c6 488bc8          mov     rcx,rax
00000000`001bf5c9 33d2            xor     edx,edx
00000000`001bf5cb ff1567020000    call    qword ptr [00000000`001bf838]
00000000`001bf5d1 eb13            jmp     00000000`001bf5e6
00000000`001bf5d3 ff154f020000    call    qword ptr [00000000`001bf828]
00000000`001bf5d9 488d4c2420      lea     rcx,[rsp+20h]
00000000`001bf5de 8bd0            mov     edx,eax
00000000`001bf5e0 ff1562020000    call    qword ptr [00000000`001bf848]
00000000`001bf5e6 488b5c2470      mov     rbx,qword ptr [rsp+70h]
00000000`001bf5eb 4883c460        add     rsp,60h
00000000`001bf5ef 5f              pop     rdi
00000000`001bf5f0 c3              ret

0:000> u rip l10
00000000`001ef660 48895c2408      mov     qword ptr [rsp+8],rbx
00000000`001ef665 57              push    rdi
00000000`001ef666 4883ec60        sub     rsp,60h
00000000`001ef66a 0f10055f020000  movups  xmm0,xmmword ptr [00000000`001ef8d0]
00000000`001ef671 488b0550020000  mov     rax,qword ptr [00000000`001ef8c8]
00000000`001ef678 0f100d61020000  movups  xmm1,xmmword ptr [00000000`001ef8e0]
00000000`001ef67f 4889442478      mov     qword ptr [rsp+78h],rax
00000000`001ef684 8a0576020000    mov     al,byte ptr [00000000`001ef900]
00000000`001ef68a 488bf9          mov     rdi,rcx
00000000`001ef68d 88442450        mov     byte ptr [rsp+50h],al
00000000`001ef691 0f11442420      movups  xmmword ptr [rsp+20h],xmm0
00000000`001ef696 0f100553020000  movups  xmm0,xmmword ptr [00000000`001ef8f0]
00000000`001ef69d 0f114c2430      movups  xmmword ptr [rsp+30h],xmm1
00000000`001ef6a2 0f11442440      movups  xmmword ptr [rsp+40h],xmm0
00000000`001ef6a7 ff158b020000    call    qword ptr [00000000`001ef938]
00000000`001ef6ad 8bc8            mov     ecx,eax
0:000> pc
00000000`001ef6a7 ff158b020000    call    qword ptr [00000000`001ef938] ds:00000000`001ef938={kernel32!GetLastErrorStub (00000000`771e2d60)}
0:000>
00000000`001ef6af e86cffffff      call    00000000`001ef620
0:000>
00000000`001ef6c7 ff158b020000    call    qword ptr [00000000`001ef958] ds:00000000`001ef958=ffffffffff2a7e28
0:000> dc 00000000`001ef958
00000000`001ef958  ff2a7e28 ffffffff 00000000 00000000  (~*.............
00000000`001ef968  00000000 00000000 00000000 00000000  ................
00000000`001ef978  00000000 00000000 00000000 00000000  ................
00000000`001ef988  00000000 00000000 00000000 00000000  ................
00000000`001ef998  00000000 00000000 00000000 00000000  ................
00000000`001ef9a8  00000000 00000000 00000000 00000000  ................
00000000`001ef9b8  00000000 00000000 00000000 00000000  ................
00000000`001ef9c8  00000000 00000000 00000000 00000000  ................
0:000> p
(1558.16e8): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
ffffffff`ff2a7e28 ??              ???
0:000>

/*
 * Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
 *
 * LGPL.
 */


# ifdef DECLARE
# undef DECLARE
# endif /* DECLARE */

# include "syscall.h"


/* pid_t getpid(void); */
/* pid_t getppid(void); */
syscall0(pid_t, getpid)
syscall0(pid_t, getppid)

/* uid_t getuid(void); */
/* uid_t geteuid(void); */
syscall0(uid_t, getuid)
syscall0(uid_t, geteuid)

/* gid_t getgid(void); */
/* gid_t getegid(void); */
syscall0(gid_t, getgid)
syscall0(gid_t, getegid)

/* pid_t fork(void); */
syscall0(pid_t, fork)


/* void _exit(int status) */
syscall1(void, exit, int, status)

/* time_t time(time_t *tloc) */
syscall1(time_t, time, time_t *, tloc)

/* pid_t getpgid(pid_t pid); */
syscall1(pid_t, getpgid, pid_t, pid)

/* int rmdir(const char *pathname); */
syscall1(int, rmdir, const char *, pathname);

/* int close(int fd); */
syscall1(int, close, int, fd);

/* pid_t wait(int *status) */
/* syscall1(pid_t, wait, int *, status); */


/* int stat(const char *pathname, struct stat *buf); */
syscall2(int, stat, const char *, pathname, struct stat *, buf)
/* int mkdir(const char *pathname, mode_t mode); */
syscall2(int, mkdir, const char *, pathname, mode_t, mode)


/* ssize_t write(int fd, const void *buf, size_t count); */
syscall3(ssize_t, write, int, fd, const void *, buf, size_t, count)
/* ssize_t read(int fd, void *buf, size_t count); */
syscall3(ssize_t, read, int, fd, const void *, buf, size_t, count)
/* int execve(const char *filename, char *const argv[], */
/*                   char *const envp[]); */
syscall3(int, execve, const char *, filename, char *const *, argv,
         char *const *, envp)
/* int open(const char *pathname, int flags, mode_t mode); */
syscall3(int, open, const char *, pathname, int, flags, mode_t, mode)

# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# include <assert.h>

# include <unistd.h>
# endif

# include "syscall.h"


int
main(void)
{
  fprintf(stdout, "getpid: %d == %d\n", getpid(), ic_getpid());
  assert(getpid() == ic_getpid());
  fprintf(stdout, "getppid: %d == %d\n", getppid(), ic_getppid());
  assert(getppid() == ic_getppid());

  fprintf(stdout, "getuid: %d == %d\n", getuid(), ic_getuid());
  assert(getuid() == ic_getuid());
  fprintf(stdout, "geteuid: %d == %d\n", geteuid(), ic_geteuid());
  assert(geteuid() == ic_geteuid());

  fprintf(stdout, "getgid: %d == %d\n", getgid(), ic_getgid());
  assert(getgid() == ic_getgid());
  fprintf(stdout, "getegid: %d == %d\n", getegid(), ic_getegid());
  assert(getegid() == ic_getegid());

  return EXIT_SUCCESS;
}

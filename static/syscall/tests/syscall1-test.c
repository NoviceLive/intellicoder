# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# include <assert.h>

# include <unistd.h>
# include <time.h>
# endif

# include "syscall.h"


int
main(void)
{
  fprintf(stdout, "time: %d == %d\n", time(NULL), ic_time(NULL));

  fprintf(stdout, "getpgid: %d == %d\n",
          getpgid(getpid()), ic_getpgid(ic_getpid()));

  ic_exit(0);

  return EXIT_FAILURE;
}

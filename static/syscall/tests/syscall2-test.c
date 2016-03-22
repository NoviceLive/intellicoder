# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# include <errno.h>

# include <unistd.h>
# endif

# include "syscall.h"


int
main(void)
{
  char *names[] = { "./makefile", "./syscall.h" };
  struct stat info, mine;

  fprintf(stdout, "%p %p\n", &info, &mine);

  for (int i = 0; i < 2; i += 1) {
    int ret;
    if ((ret = stat(names[i], &info)) != 0) {
      perror("stat");
    }
    else if ((ret = ic_stat(names[i], &mine)) != 0) {
      errno = -ret;
      perror("ic_stat");
    }
    else {
      fprintf(stdout, "stat.st_ino: %d %d\n",
              info.st_ino, mine.st_ino);
      fprintf(stdout, "stat.st_size: %d %d\n",
              info.st_size, mine.st_size);
    }
  }

  return EXIT_SUCCESS;
}

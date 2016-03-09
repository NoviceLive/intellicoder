# ifndef CPP
# include <stdlib.h>

# include <unistd.h>
# endif /* CPP */


int
main(void)
{
  char bin[] = "/bin/sh";
  execve(bin, NULL, NULL);
  return EXIT_SUCCESS;
}

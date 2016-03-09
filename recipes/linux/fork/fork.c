# ifndef CPP
# include <stdlib.h>

# include <unistd.h>
# endif /* CPP */


int
main(void)
{

  pid_t pid = fork();

  if (pid >= 0) {
    if (pid == 0) {
      write(STDOUT_FILENO, "This is Child\n",
            sizeof "This is Child\n");
    }
    else {
      write(STDOUT_FILENO, "This is Parent\n",
            sizeof "This is Parent\n");
    }
  }
  else {
    write(STDOUT_FILENO, "Fork Failed\n", sizeof "Fork Failed\n");
  }

  return EXIT_SUCCESS;
}

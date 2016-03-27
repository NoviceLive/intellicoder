# ifndef CPP
# include <stdlib.h>

# include <unistd.h>
# endif /* CPP */


int
main(void)
{
  /* char message[] = "Hello World!\n"; */
  /* write(STDOUT_FILENO, message, sizeof message); */

  write(STDOUT_FILENO, "Hello World!\n", sizeof "Hello World!\n");

  return EXIT_SUCCESS;
}

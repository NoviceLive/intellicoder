# ifndef CPP
# include <stdlib.h>

# include <unistd.h>
# endif /* CPP */


int
main(void)
{
  char buf[256];
  char message[] = "Enter something: ";
  write(STDIN_FILENO, message, sizeof message);
  size_t count = read(STDIN_FILENO, buf, 20);
  if (count > 0) {
    write(STDOUT_FILENO, buf, count);
  }

  return EXIT_SUCCESS;
}

# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# include <errno.h>

# include <unistd.h>
# include <fcntl.h>
# endif

# include "syscall.h"


int ATTR
main(void)
{
  /* char msg[] = "Hello World!\n"; */
  /* ssize_t ret; */
  /* ret = write(2, msg, sizeof msg); */
  /* printf("ret: %zu == %zu\n", ret, sizeof msg); */

  /* ret = ic_write(2, msg, sizeof msg); */
  /* printf("ret: %zu == %zu\n", ret, sizeof msg); */

  /* char buf[15] = { 0 }; */
  /* printf("%s", "read: "); */
  /* fflush(stdout); */
  /* ret = read(1, buf, sizeof buf); */
  /* write(2, buf, ret); */

  /* printf("%s", "ic_read: "); */
  /* fflush(stdout); */
  /* ret = ic_read(1, buf, sizeof buf); */
  /* ic_write(2, buf, ret); */


  /* execve("./bin/syscall0-test", NULL, NULL); */
  /* ic_execve("./bin/syscall0-test", NULL, NULL); */


  char *names[] = { "makefile", "none" };
  for (int i = 0; i < 2; i += 1) {
    int fd = ic_open(names[i], O_RDONLY, 0);
    printf("fd for %s: %d\n", names[i], fd);
    if (fd >= 0) {
      char buf[400];
      ssize_t ret = ic_read(fd, buf, sizeof buf);
      ic_write(STDIN_FILENO, buf, ret);
      ic_close(fd);
    }
    else {
      errno = -fd;
      perror("ic_open");
    }
  }


  return EXIT_SUCCESS;
}

# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# include <errno.h>

# include <unistd.h>
# include <sys/syscall.h>
# include <sys/stat.h>
# endif

# ifdef __i386__
static int
ic_mkdir(const char * pathname, mode_t mode)
{
  long result;
  __asm__ volatile ("int $0x80"
                    : "=a" (result)
                    : "a" (SYS_mkdir),
                      "b" ((long)pathname),
                      "c" ((long)mode));
  return result;
}
# endif

# ifdef __amd64__
static int
ic_mkdir(const char * pathname, mode_t mode)
{
  long result;
  __asm__ volatile ("syscall"
                    : "=a" (result)
                    : "a" (SYS_mkdir),
                      "D" ((long)pathname),
                      "S" ((long)mode));
  return result;
}
# endif


int
main(void)
{
  char *dirs[] = { "test1", "foobar" };
  for (int i = 0; i < 2; i += 1) {
    int ret = ic_mkdir(dirs[i], S_IRWXU | S_IRGRP);
    fprintf(stderr, "ret: %d\n", ret);
    if (ret != 0) {
      errno = -ret;
      perror("ic_mkdir");
    }

    ret = mkdir(dirs[i], S_IRWXU | S_IRGRP);
    fprintf(stderr, "ret: %d\n", ret);
    if (ret != 0) {
      perror("mkdir");
    }
  }

  return EXIT_SUCCESS;
}

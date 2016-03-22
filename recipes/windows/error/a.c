# include <stdlib.h>

# include <windows.h>

# include "stdafx.h"
# include "libwinerror.h"


# define SIZE 1024


int
main(void)
{
  IMAGE_DOS_HEADER dos;
  DWORD written;
  HANDLE con = GetStdHandle(STD_OUTPUT_HANDLE);
  FILE *fp = fopen("sc32.exe", "r");
  fread(&dos, 1, sizeof dos, fp);
  WriteConsoleA(con, &dos, sizeof dos, &written, NULL);
  CloseHandle(con);
  return EXIT_SUCCESS;
}

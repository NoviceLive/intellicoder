# include <stdlib.h>

# include <windows.h>


int main(void)
{
  WIN32_FIND_DATA found;
  DWORD size;
  HANDLE con = GetStdHandle(STD_OUTPUT_HANDLE);
  HANDLE dir = FindFirstFileA(".\\*", &found);
  if (dir == INVALID_HANDLE_VALUE) {
    return EXIT_FAILURE;
  }
  do {
    WriteConsoleA(con,
                  found.cFileName,
                  strlen(found.cFileName),
                  &size,
                  NULL);
    /* putchar('\n'); */
  }
  while (FindNextFileA(dir, &found));
  FindClose(dir);
  return EXIT_SUCCESS;
}

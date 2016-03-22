# include <windows.h>
# include <string.h>

# include "libwinerror.h"


void
print_last_error(void)
{
  CHAR *string;
  DWORD number;
  number = FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER
                         | FORMAT_MESSAGE_FROM_SYSTEM
                         | FORMAT_MESSAGE_IGNORE_INSERTS,
                         NULL, GetLastError(),
                         MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
                         (CHAR *)&string, 0, NULL);
  DWORD written;
  HANDLE con = GetStdHandle(STD_OUTPUT_HANDLE);
  if (number) {
    WriteConsoleA(con, string, number, &written, NULL);
    HeapFree(GetProcessHeap(), 0, string);
  }
  else {
    WriteConsoleA(con, "unknwon error", strlen("unknown error"),
                  &written, NULL);
  }
  return;
}

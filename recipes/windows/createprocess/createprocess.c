# include <windows.h>


void
main(void)
{
  STARTUPINFO si = { 0 };
  PROCESS_INFORMATION pi = { 0 };

  if (!CreateProcessA(NULL, "calc",
                      NULL, NULL, FALSE, 0, NULL, NULL,
                      &si, &pi)) {
    return;
  }

  /* WaitForSingleObject(pi.hProcess, INFINITE); */
  /* CloseHandle(pi.hProcess); */
  /* CloseHandle(pi.hThread); */

  return;
}

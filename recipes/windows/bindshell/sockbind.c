# include <stdio.h>

# include <windows.h>


void
main(void)
{
  WSADATA wsa = { 0 };
  int error = 0;
  SOCKET server, client;
  SOCKADDR_IN addr, client_addr;
  char buf[1024];

  error = WSAStartup(MAKEWORD(2, 2), &wsa);
  if (error) {
    printf("%d\n", WSAGetLastError());
    return;
  }

  server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (server == INVALID_SOCKET) {
    printf("%d\n", WSAGetLastError());
  }
  else {
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(8000);
    error = bind(server, (SOCKADDR *)&addr, sizeof addr);
    if (error) {
      printf("%d\n", WSAGetLastError());
    }
    else {
      error = listen(server, SOMAXCONN);
      if (error) {
        printf("%d\n", WSAGetLastError());
      }
      else {
        client = accept(server, (SOCKADDR *)&client_addr, NULL);
        if (client == INVALID_SOCKET) {
          printf("%d\n", WSAGetLastError());
        }
        else {
          do {
            error = recv(client, buf, sizeof buf, 0);
            if (error > 0) {
              buf[error] = '\0';
              printf("%s", buf);
            }
            else if (error == 0) {
              printf("%s\n", "closed");
            }
            else {
              printf("%d\n", WSAGetLastError());
            }
          }
          while (error > 0);
        }
      }
      error = closesocket(server);
      if (error) {
        printf("%d\n", WSAGetLastError());
      }
    }
  }

  error = WSACleanup();
  if (error) {
    printf("%d\n", WSAGetLastError());
    return;
  }

  return;
}

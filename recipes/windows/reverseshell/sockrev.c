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

  error = WSAStartup(MAKEWORD(2, 2), &wsa);
  if (error) {
    return;
  }

  client = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (client == INVALID_SOCKET) {
    return;
  }

  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = inet_addr("192.168.56.1");
  addr.sin_port = htons(8000);
  error = connect(client, (SOCKADDR *)&addr, sizeof addr);
  if (error) {
    return;
  }

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

  return;
}

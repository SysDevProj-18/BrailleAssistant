#include <liblouis.h>
#include <locale.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <wctype.h>

void toWideChar(const char *str, widechar *wstr) {
  int i = 0;
  while (str[i] != '\0') {
    wstr[i] = (widechar)str[i];
    i++;
  }
  wstr[i] = L'\0';
}

int main() {
  lou_setLogLevel(LOU_LOG_ALL);
  setlocale(LC_ALL, "");
  const char *tableList = "en-GB-g2.ctb";
  const char *str = "apple";
  widechar inbuf[100];
  toWideChar(str, inbuf);
  int inlen = strlen(str);
  widechar outbuf[100];
  int outlen = 100;
  int mode = 68;
  int err = lou_translateString(tableList, inbuf, &inlen, outbuf, &outlen, NULL,
                                NULL, mode);
  if (err == 0) {
    // error
    printf("error");
  }
  printf("1");
  printf("%lc\n", outbuf[0]);
  printf("Program finished\n");
  lou_free();
  return 0;
}

#include <liblouis.h>
#include <locale.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>

void toWideChar(const char *str, widechar *wstr) {
  int i = 0;
  while (str[i] != '\0') {
    wstr[i] = (widechar)str[i];
    i++;
  }
  wstr[i] = L'\0';
}
// args
int main(int argc, char *argv[]) {
  lou_setLogLevel(LOU_LOG_OFF);
  setlocale(LC_ALL, "");
  const char *tableList = "en-GB-g2.ctb";
  const char *str = argv[1];
  // set the length of inbuf to the length of the string
  widechar inbuf[strlen(str)];
  toWideChar(str, inbuf);
  int inlen = strlen(str);
  widechar outbuf[strlen(str) * 2];
  int outlen = 100;
  int mode = 68;
  int err = lou_translateString(tableList, inbuf, &inlen, outbuf, &outlen, NULL,
                                NULL, mode);
  if (err == 0) {
    // error
    printf("error");
  }
  for (int i = 0; i < outlen; i++) {
    printf("%lc", outbuf[i]);
  }
  lou_free();
  return 0;
}

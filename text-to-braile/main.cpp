#include <liblouis.h>
#include <stdio.h>

int main() {
  const char *tableList = "en-us-g2.ctb";
  const widechar inbuf[] = {L'c', L'a', L't', L'\0'};
  int inlen = 4;
  widechar outbuf[100];
  int outlen = 100;
  formtype typeform;
  char spacing[100];
  translationModes mode = dotsIO;
  lou_translateString(tableList, inbuf, &inlen, outbuf, &outlen, &typeform,
                      spacing, mode);
  printf("outlen: %d\n", outlen);
  // print outbuf[0] to outbuf[outlen-1]
  for (int i = 0; i < outlen; i++) {
    printf("%c", (char)outbuf[i]);
  }
  // print
  // std::cout << "outbuf: " << outbuf << std::endl;
  //  for (auto w : outbuf) {
  //    printf("%c", (char)w);
  //  }
  lou_free();
  return 0;
}

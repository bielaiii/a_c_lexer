/* asds dasd asd jlksdfjs
sdfjsdlk
*/
// asdas
// asdasd

#include <stdio.h>
#include <stdlib.h>

typedef struct {
  int a;
  unsigned char b;
} foo;
typedef struct {
  foo f_;
  long long a;
  // float (*ptr)[3][3];
  // double arr[3];
  int (*ptrr)[3];
  float asd[3];
} bar;

void func(bar *b, int a)
{

}


int main() {
  bar b[3] = {{.ptrr = NULL, 1, .f_.a = 1, .f_.b = 2, .asd = {1, 2, 3}},
              {.ptrr = NULL, 2, .f_.a = 3, .f_.b = 4, .asd = {4, 5, 6}},
              {.ptrr = NULL, 3, .f_.a = 5, .f_.b = 6, .asd = {7, 8, 9}}};
  printf("%d %d %d\n", b[0].f_.a, b[1].f_.a, b[2].f_.a);
  printf("%d %d %d\n", b[0].f_.b, b[1].f_.b, b[2].f_.b);
  printf("%d %d %d\n", b[0].ptrr, b[1].ptrr, b[2].ptrr);
  if (0) {
    printf("hello, world\n");
  }
  // printf("%d %d %d\n", b[0].f_.a, b[1].f_.a, b[2].f_.a);
  return 0;
}

typedef struct {
  int a;
  int (*arr)[3];
  unsigned char b;
#if 0
  //fake_struct nn;
#endif
} foo, *fp, fp3[3][22];

int int_arr[3] = {1, 2, 3};

foo f1[] = {{.a = 1, .arr = &int_arr, .b = 2}, {3, &int_arr, 4}, {.a  = 8, &int_arr, 4}};
int main() {
  return 0;
}

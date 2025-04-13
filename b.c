#include<stdio.h>
#include<stdlib.h>

typedef struct {
  int a;
  int (*arr)[3];
  unsigned char b;

} foo;

typedef struct {
    foo f;
    unsigned long long num;
    int *ptr;
}bar;

foo f1[] = {{.a = 1, .arr = &int_arr, .b = 2}, {3, &int_arr, 4}, {.a  = 8, &int_arr, 4}};
int int_arr[3] = {1, 2, 3};

//bar b_ = {{1, &int_arr}, .num = 10, .ptr = NULL};
//bar bb = {1, &int_arr, .num = 10, .ptr = NULL};



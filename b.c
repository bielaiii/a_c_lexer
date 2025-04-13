#include<stdio.h>
#include<stdlib.h>

typedef struct {
  int a;
  int (*arr)[3];
  unsigned char b;

} foo;

typedef struct {
  int a;
  //int (*arr)[3];
  long long  b;
  long long c;

} foocfg;
typedef struct {
  int a;
  //int (*arr)[3];
  unsigned char b;
  long long c;

} fooreg;
typedef struct {
    foo f;
    unsigned long long num;
    int *ptr;
}bar;

//foo f1[] = {{.a = 1, .arr = &int_arr, .b = 2}, {3, &int_arr, 4}, {.a  = 8, &int_arr, 4}};
//int int_arr[3] = {1, 2, 3};

//bar b_ = {{1, &int_arr}, .num = 10, .ptr = NULL};
//bar bb = {1, &int_arr, .num = 10, .ptr = NULL};
int init_func(fooreg * reg, foocfg *cfg)
{
    int arr[3] = {1, 2, 3};
    reg->a = cfg->a;
    reg->b = cfg->b;
    reg->c = cfg->c;
    if (0)  
        while (1) {
        
        }

    
    return 0;
}



#include<stdlib.h>
#include<stdio.h>


typedef struct {
    int a;
    unsigned char b;
} foo;
typedef struct {
    foo f_;
    long long a;
    float (*ptr)[3][3];
} bar;


bar b = {0, 1, 2, 0};
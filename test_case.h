#ifndef TEST_HEADER_H
#define TEST_HEADER_H

// 基本数据类型声明
int basic_int;
float basic_float;
double basic_double;
char basic_char;
unsigned int basic_unsigned_int;
signed char basic_signed_char;

// 结构体声明
struct SimpleStruct {
    int member1;
    float member2;
};

// 带标签的结构体声明
typedef struct TaggedStruct {
    char *str;
    struct SimpleStruct nested;
} TaggedStruct;

// 联合声明
union SimpleUnion {
    int int_val;
    float float_val;
};

// 枚举声明
enum SimpleEnum {
    ENUM_VAL1,
    ENUM_VAL2,
    ENUM_VAL3
};

// 函数声明
int add(int a, int b);
float divide(float a, float b);

// 函数指针声明
typedef int (*FunctionPointer)(int, int);

// 数组声明
int int_array[10];
char char_array[20];

// 常量声明
const int CONST_INT = 10;
const float CONST_FLOAT = 3.14f;

// 静态变量声明
static int static_var = 0;

// 外部变量声明
extern int external_var;

// 复杂类型声明
struct ComplexStruct {
    int *int_ptr;
    struct TaggedStruct *tagged_ptr;
    union SimpleUnion union_member;
    enum SimpleEnum enum_member;
    FunctionPointer func_ptr;
    int multi_dim_array[2][3];
};

// 预处理器指令示例
#ifdef DEBUG
#define DEBUG_PRINT(x) printf("%s\n", x)
#else
#define DEBUG_PRINT(x)
#endif

#endif // TEST_HEADER_H
#include <stdio.h>
#include <stdlib.h>

#define MAX_LEN 100

#define MAX(a, b) ((a) > (b) ? (a) : (b))


extern "C" {

    /* Function to compute factorial recursively */
    int factorial(int n) {
        if (n <= 1) return 1;
        else return n * factorial(n - 1);
    }
    
}
// Main function
int main() {
    int num = 5;
    long result = factorial(num);
    printf("Factorial of %d is %ld\n", num, result);

    // Dynamic memory allocation
    int* arr = (int*)malloc(MAX_LEN * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "Memory allocation failed!\n");
        return 1;
    }

    for (int i = 0; i < MAX_LEN; i++) {
        arr[i] = i * i;
    }

    free(arr);
    return 0;
}
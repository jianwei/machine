#include <stdio.h>
#include <unistd.h>
#include <string.h>


int main(int argc, char const *argv[])
{
    /* code */
    // printf("12");
    double a=32767;
    int b=1234;
    int c = b/a *100;

    printf ("c:%d",c);
    return 0;
}


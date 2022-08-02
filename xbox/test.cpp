#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

using namespace std;

int main(int argc, char const *argv[])
{
    double a=32767;
    int b=abs(-1234);
    float c = b/a;
    double d = 1.0/3.0;
    printf ("a:%f,b:%d,c:%f,d:%f",a,b,c,d);

    return 0;
}


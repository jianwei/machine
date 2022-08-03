#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

using namespace std;
void a();
void b();


int main()
{
    a();
    float z=100;
    double angle = atan(z) * 180.0/3.1415926;
    printf("s:%f",angle);
    return 0;
}
void b(){
    printf("b");
}
void a(){
    printf("a");
    b();
}


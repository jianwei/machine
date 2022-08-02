#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

using namespace std;
void a();
void b();


int main()
{
    a();
    return 0;
}
void b(){
    printf("b");
}
void a(){
    printf("a");
    b();
}


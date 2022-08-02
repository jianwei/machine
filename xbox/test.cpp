#include <stdio.h>
#include <unistd.h>
#include <string.h>

using namespace std;

int main(int argc, char const *argv[])
{
    double a=32767;
    int b=1234;
    float c = b/a *100;
    char d[] = "aaaa ";
    char f[]="";
    // char f[] = (string) b+d;
    sprintf(f,"%s,%d",d,b);
    if(b>0 && a<0)
    {
        printf ("d:%s",f);
    }
    
    return 0;
}


#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <iostream>
#include <math.h>

using namespace std;

void exec_shell(char* cmd, char* &ret){
    char buf[80];
    char* cmd_all;   
    getcwd(buf,sizeof(buf));
    cout << buf << endl;
    sprintf(cmd_all, "cd %s/../center/ &&  python3 scripts.py %s",buf,cmd);
    cout << cmd_all << endl;
    // FILE *fp;
    char buffer[80]; 
    
    fp = popen(cmd_all,"r");
    fgets(buffer,sizeof(buffer),fp);
    pclose(fp);
    ret = buffer;
}


int main () {
    char* val;
    char cmd[] = "--type 1 --cmd 1";
    exec_shell(cmd,val);

   return(0);
}


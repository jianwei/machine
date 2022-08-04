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

// void exec_shell(char* cmd, char* &ret){
//     char buf[80];
//     char* cmd_all;   
//     getcwd(buf,sizeof(buf));
//     cout << buf << endl;
//     sprintf(cmd_all, "cd %s/../center/ &&  python3 scripts.py %s",buf,cmd);
//     cout << cmd_all << endl;
//     // FILE *fp;
//     char buffer[80]; 
    
//     FILE *fp; 
//     fp = popen(cmd_all,"r");
//     fgets(buffer,sizeof(buffer),fp);
//     pclose(fp);
//     ret = buffer;
// }
char* global_pwd;

void exec_shell(char params[], char* &ret){
    cout<<2<<endl;
    char* cmd_all;
    if(strlen(global_pwd)==0){
        char buf[80];
        getcwd(buf,sizeof(buf));
        sprintf(global_pwd, "%s",buf);
    }
    cout<<123<<global_pwd<<params<<endl;
    snprintf(cmd_all,128, "cd %s/../center/ &&  python3 scripts.py %s",global_pwd,params);
    cout<<cmd_all<<endl;

    FILE *fp;
    char buffer[80]; 
    fp = popen(cmd_all,"r");
    fgets(buffer,sizeof(buffer),fp);
    pclose(fp);
    ret = buffer;
    cout << "script:"<<cmd_all << ",vaule:"<<buffer <<endl;
}


int main () {
    char* val;
    char cmd[] = "--type 2 --dict {\"begin_work\":1}";
    exec_shell(cmd,val);

   return(0);
}


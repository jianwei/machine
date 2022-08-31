#include <stdio.h>
#include <string.h> 

void split(char *src,const char *separator,char **dest,int *num) {
     char *pNext;
     //记录分隔符数量 
     int count = 0;
     //原字符串为空 
     if (src == NULL || strlen(src) == 0)
        return;
    //未输入分隔符
     if (separator == NULL || strlen(separator) == 0)
        return;   
	/*
		c语言string库中函数，
		声明： 
		char *strtok(char *str, const char *delim)
		参数： 
	    str -- 要被分解成一组小字符串的字符串。
    	delim -- 包含分隔符的 C 字符串。
    	返回值：
		该函数返回被分解的第一个子字符串，如果没有可检索的字符串，则返回一个空指针。 

	*/
	char *strtok(char *str, const char *delim); 
	 //获得第一个由分隔符分割的字符串 
    pNext = strtok(src,separator);
    while(pNext != NULL) {
     	//存入到目的字符串数组中 
        *dest++ = pNext; 
        ++count;
        /*
			strtok()用来将字符串分割成一个个片段。参数s指向欲分割的字符串，参数delim则为分割字符串中包含的所有字符。
			当strtok()在参数s的字符串中发现参数delim中包涵的分割字符时,则会将该字符改为\0 字符。
			在第一次调用时，strtok()必需给予参数s字符串，往后的调用则将参数s设置成NULL。
			每次调用成功则返回指向被分割出片段的指针。

		*/  
        pNext = strtok(NULL,separator);  
    }  
    *num = count;
}    

//将一串以空格为分割线的字符串分开，数据存到一个二维数组中去 
int main(){
	char str[100]="find\nthe\nway";
	char *p[8]={0};
	int num=0,i;
	// gets(str);
	//attention!!!!! 这里的分隔符已定要写为字符串的形式。 
	split(str,"\n",p,&num);
    printf("%s\n",p[num-1]);
	// for(i = 0;i < num; i ++) {
    //     printf("%s\n",p[i]);
    // }
    return 0;
} 

 

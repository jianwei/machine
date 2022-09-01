#include <stdio.h>
#include <string.h>
#include <hiredis/hiredis.h>
#include <iostream>

#include <sstream>
using namespace std;
//将一串以空格为分割线的字符串分开，数据存到一个二维数组中去
int main()
{
	redisContext *rc;
	struct timeval timeout = {1, 500000}; // 1.5 seconds
	rc = redisConnectWithTimeout("127.0.0.1", 6379, timeout);

	char *key = (char *)"str";
	char *val = (char *)"Hello World";

	// redisReply *reply;
	// reply = (redisReply *)redisCommand(rc, "SET %s %s", key, val);
	// freeReplyObject(reply);

	redisReply *reply2;
	reply2 = (redisReply *)redisCommand(rc, "GET %s", key);
	cout << "get string type = " << reply2->type << endl;
	printf("type:%d,%d\n", reply2->type, REDIS_REPLY_STRING);
	printf("len:%ld\n", reply2->len);
	printf("str1:%s,%d\n", reply2->str, reply2->str == NULL);
}

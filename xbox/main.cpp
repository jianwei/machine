#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <hiredis/hiredis.h>

int main()
{
	redisContext * rc = redisConnect("127.0.0.1",6379);
	assert(rc != NULL);
	
	char* com = "hmset user name jack age 18 sex male height 180";
	redisReply* res =(redisReply*)redisCommand(rc,com);

	if(res->type == REDIS_REPLY_STATUS)
	{
		printf("Success %s\n",res->str);
	}
	else 
		printf("fail\n");
	
	com = "hgetall user";
	res = (redisReply*)redisCommand(rc,com);
	if(res->type == REDIS_REPLY_ARRAY)
	{
		for(int i = 0; i < res->elements; i++)
		{
			if(i%2 != 0)
				printf("%s\n",res->element[i]->str);
			else
				printf("%s",res->element[i]->str);
		}
	}
	else if(res->type == REDIS_REPLY_STRING)
	{
		printf("%s",res->str);
	}
	
	freeReplyObject(res);
	redisFree(rc);
	return 1;
}


#include "stdio.h"
#include "string.h"
#include "stdlib.h"
#include "redisCli.h"
 
static redisContext *redisCliConn = NULL;
 
 
int redisCliInit(void )
{
	redisCliConn  = redisConnect("127.0.0.1",6379);
	if(redisCliConn != NULL && redisCliConn->err)
	{
		printf("redisCliInit connection error: %s\n",redisCliConn->errstr);
		redisFree(redisCliConn);
		redisCliConn = NULL;
		return -1;
	}
	return 0;
}
 
 
int redisCliClose(void )
{
	if(redisCliConn)
	{
		redisFree(redisCliConn);
		redisCliConn = NULL;
	}
	return 0;
}
 
 
 
int redisCliKeyValueGet(char *cpFindName,char *cpFindValue,int valueLen)
{
	redisReply *reply;
	
	if(cpFindName == NULL || cpFindValue == NULL)
	{
		printf("redisCliKeyValueGet failed in param is null\r\n");
		return -1;
	}
	
	if(redisCliConn == NULL)
	{
		if(0 != redisCliInit())
		{
			return -1;
		}
	}
	
	reply = (redisReply *)redisCommand(redisCliConn,"GET %s",cpFindName);
	if(reply == NULL || redisCliConn->err)
	{
		printf("redisCliKeyValueGet reply is error\r\n");
		redisFree(redisCliConn);
		redisCliConn = NULL;		
		return -1;
	}
	else
	{
		if((reply->type == REDIS_REPLY_STRING) && (reply->str))
		{
			memcpy(cpFindValue,reply->str,
					(strlen(reply->str) >= valueLen) ? (valueLen - 1) : strlen(reply->str));
			freeReplyObject(reply);
			return 0;
		}
		else
		{
			printf("reply->type == REDIS_REPLY_ERROR\r\n");
			freeReplyObject(reply);
			redisFree(redisCliConn);
			redisCliConn = NULL;
			return -1;
		}
	}
}
 
 
int redisCliKeyValueSet(char *cpFindName,char *cpFindValue)
{
	redisReply *reply;
	
	if(cpFindName == NULL || cpFindValue == NULL)
	{
		printf("redisCliKeyValueSet failed in param is null\r\n");
		return -1;
	}
	
	if(redisCliConn == NULL)
	{
		if(0 != redisCliInit())
		{
			return -1;
		}
	}
	
	reply = (redisReply *)redisCommand(redisCliConn,"SET %s %s",cpFindName,cpFindValue);
	if(reply == NULL || redisCliConn->err)
	{
		printf("redisCliKeyValueSet reply is null\r\n");
		redisFree(redisCliConn);
		redisCliConn = NULL;		
		return -1;
	}
	else
	{
		if(reply->type == REDIS_REPLY_ERROR)
		{
			printf("reply->type == REDIS_REPLY_ERROR\r\n");
			freeReplyObject(reply);
			redisFree(redisCliConn);
			redisCliConn = NULL;
			return -1;
		}
		else
		{
			freeReplyObject(reply);
			return 0;			
		}
	}	
}
 
 
 
int redisCliKeyValuePublish(char *cpFindName,char *cpFindValue)
{
	redisReply *reply;
	
	if(cpFindName == NULL || cpFindValue == NULL)
	{
		printf("redisCliKeyValueSet failed in param is null\r\n");
		return -1;
	}
	
	if(redisCliConn == NULL)
	{
		if(0 != redisCliInit())
		{
			return -1;
		}
	}
 
	reply = (redisReply *)redisCommand(redisCliConn,"PUBLISH %s %s",cpFindName,cpFindValue);
	if(reply == NULL || redisCliConn->err)
	{
		printf("redisCliKeyValueSet reply is null\r\n");
		redisFree(redisCliConn);
		redisCliConn = NULL;		
		return -1;
	}
	else
	{
		if(reply->type == REDIS_REPLY_ERROR)
		{
			printf("reply->type == REDIS_REPLY_ERROR\r\n");
			freeReplyObject(reply);
			redisFree(redisCliConn);
			redisCliConn = NULL;
			return -1;
		}
		else
		{
			freeReplyObject(reply);
			return 0;			
		}
	}	
}
 
 
 
 
 
/*此函数调用会卡住一直执行while，一直等待服务器的发布*/
void redisCliSubscribe()
{
	int i = 0;
	redisReply* reply;
	
	printf("connect redis server:%s,port:%d,SUBSCRIBE channel:%s\n", "127.0.0.1", 6379, "adminCard");
	redisContext* context = redisConnect("127.0.0.1", 6379);  //链接本地127.0.0.1，端口为6379的redis
	
	reply = redisCommand(context, "SUBSCRIBE %s","adminCard");
	freeReplyObject(reply);
	while (redisGetReply(context,(void **)&reply) == REDIS_OK)
	{
		if (reply)
		{
			switch (reply->type)
			{
				case REDIS_REPLY_ERROR:
				case REDIS_REPLY_STRING:
				case REDIS_REPLY_NIL:
				case REDIS_REPLY_INTEGER:
				case REDIS_REPLY_STATUS:
						break;
				case REDIS_REPLY_ARRAY:
						{
							i = 0;
							for (i = 0; i < reply->elements; ++i)
							{
									redisReply* childReply = reply->element[i];
									if (childReply->type == REDIS_REPLY_STRING)
									{
											printf("value:%s\n", childReply->str);
									}
							}
						}
						break;
				default:
						break;
			}
			freeReplyObject(reply);
		}
	}
	redisFree(context);
	return 0;
}
 
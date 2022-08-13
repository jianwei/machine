#ifndef __REDIS_CLI_H__
#define __REDIS_CLI_H__
 
#include <hiredis/hiredis.h>
 
int redisCliInit(void );
int redisCliKeyValueGet(char *cpFindName,char *cpFindValue,int valueLen);
int redisCliKeyValueSet(char *cpFindName,char *cpFindValue);
int redisCliKeyValuePublish(char *cpFindName,char *cpFindValue);
 
//subscribe看.c中的例程  REDIS_SUBSCRIBE
 
 
#endif
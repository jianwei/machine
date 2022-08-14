#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <hiredis/hiredis.h>

int main()
{

    redisContext *c;
    struct timeval timeout = {1, 500000}; // 1.5 seconds
    c = redisConnectWithTimeout("127.0.0.1", 6379, timeout);

    if (c == NULL || c->err)
    {
        if (c)
        {
            printf("Connection error: %s\n", c->errstr);
            redisFree(c);
        }
        else
        {
            printf("Connection error: can't allocate redis context\n");
        }
        exit(1);
    }
    else
    {
        printf("Success \n");
    }

    // void *reply;


    redisReply *reply;
    /* Set a key */
    reply = (redisReply *)redisCommand(c, "PUBLISH %s %s", "arduino", "---hello world----");    
    // printf("SET: %s\n", reply->str);

    freeReplyObject(reply);

    return 1;
}

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <iostream>
#include <math.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include <hiredis/hiredis.h>
using namespace std;
typedef struct xbox_map
{
    int time;
    int a;
    int b;
    int x;
    int y;
    int lb;
    int rb;
    int start;
    int back;
    int home;
    int lo;
    int ro;

    int lx;
    int ly;
    int rx;
    int ry;
    int lt;
    int rt;
    int xx;
    int yy;

} xbox_map_t;

int global_working = 0;

void set_redis(char *key, int value, redisContext *rc)
{
    cout << "set_redis" << key << value << endl;
    redisReply *reply;
    reply = (redisReply *)redisCommand(rc, "SET %s %d", key, value);
    freeReplyObject(reply);
}

void get_redis(char *key, redisContext *rc)
{

    char *get_ = (char *)malloc(32);
    sprintf(get_, "GET %s", key);
    cout << "get_redis:" << get_ << endl;
    redisReply *reply = (redisReply *)redisCommand(rc, get_);

    if (reply != NULL && reply->type == REDIS_REPLY_STRING)
    {
        // printf("%s\n", reply->str);
        cout << "get_redis-val:" << reply << reply->str << endl;
    }
    // freeReplyObject(reply); //使用reply以后必须要进行释放
}

void xbox(xbox_map_t map, char *&ret, redisContext *rc)
{
    int max = 32767;
    // char *cmd;
    char *cmd = (char *)malloc(16);
    //全局
    //机器停止
    if (map.y > 0)
    {
        ret = (char *)"STOP 0.";
        return;
    }
    //操作臂停止
    if (map.b > 0)
    {
        ret = (char *)"STOP 2.";
        return;
    }

    //开始或者关闭工作
    if (map.rb > 0)
    {
        if (global_working == 1)
        {
            global_working = 0;
            set_redis((char *)"begin_work", 0, rc);
            get_redis((char *)"begin_work", rc);
            return;
        }
        else
        {
            global_working = 1;
            set_redis((char *)"begin_work", 1, rc);
            get_redis((char *)"begin_work", rc);
            return;
        }
    }

    //非工作状态 手柄操作
    if (global_working == 0)
    {
        //复位
        if (map.a > 0)
        {
            ret = (char *)"RST.";
            return;
        }
        //后退
        if (map.ry < 0)
        {
            int val = ((float)abs(map.ry) / max) * 100;
            sprintf(cmd, "MB %d.", val);
            ret = cmd;
            return;
        }

        //前进
        if (map.ry > 0)
        {
            int val = ((float)abs(map.ry) / max) * 100;
            // cout << "MF:" << val << endl;
            sprintf(cmd, "MF %d.", val);
            ret = cmd;
            return;
        }

        //上
        if (map.yy < 0)
        {
            ret = (char *)"MU.";
            return;
        }

        //下
        if (map.yy > 0)
        {
            ret = (char *)"MD.";
            return;
        }

        //转弯
        if ((int)abs(map.ly) == max || (int)abs(map.lx) == max)
        {
            double z = (int)abs(map.lx) / (int)abs(map.ly);
            double angle = atan(z) * 180.0 / 3.1415926;
            // 左转
            if ((int)map.lx < 0 && (int)map.ly < 0)
            {
                //  cmd = self.turn(angle, 2)
            }
            // 右转
            // elif int(msgObj["LY"]) < 0 and int(msgObj["LX"]) > 0:
            if ((int)map.lx > 0 && (int)map.ly < 0)
            {
                // cmd = self.turn(angle, 1)
            }
        }
    }
}

int turn(int global_angle, int angle, int type, char *ret, redisContext *rc)
{
    global_angle = 90;
    return 0;
}

// int main()
// {
//     xbox_map_t map;
//     map.y = 12345;
//     char *ret;
//     xbox(map, ret);
//     cout << "ret:" << ret << endl;
//     return 0;
// }

// https://blog.csdn.net/persist_with/article/details/118697646
#ifndef _SERIAL_H
#define _SERIAL_H

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>

#define SERIALNAME_LEN 128

typedef struct  serial_s{
        int     fd;             //串口文件描述符
        long     Baudrate;               //波特率
        int     Databits;               //数据位
        char    Parity;         //奇偶校验位
        int     Stopbits;               //停止位
        int     mSend;          //一次发送的最大数据
        char    SerialName[SERIALNAME_LEN];     //端口名字
        struct  termios OldTermios;     //保存原来的端口配置

}serial_t;

int serial_open(serial_t *serial, char *devname, long baudrate, char *conf /*"8N1N"*/);
int serial_close(serial_t *serial);
int serial_send(serial_t *serial, char *sbuf, int sbuf_len);
int serial_recv(int fd, char *rbuf, int rbuf_len, int timeout);


#endif

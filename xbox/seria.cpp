#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <string.h>
#include <iostream>
#define File_open_USB "/dev/ttyUSB0" //串口的文件名
void serial_port_init(int fd);       //串口初始化说明
using namespace std;

int main()
{
    //1.打开串口
    char buf[1024] = "";
    int open_USB = open(File_open_USB, O_RDWR);
    if (open_USB < 0)
    {
        return -1;
    }

    //2.串口初始化
    serial_port_init(open_USB);
    while (1)
    {
        printf("请输入:");
        scanf("%s", buf);
        write(open_USB, buf, strlen(buf));
        memset(buf, 0, sizeof(buf));
        read(open_USB, buf, sizeof(buf) - 1);
        printf("接受的数据是:%s\n", buf);
        memset(buf, 0, sizeof(buf));
    }

    return 0;
}

// https://www.cnblogs.com/wang1299/p/14548339.html
// char writeMsg(string msg){
char writeMsg(string msg)
{
    printf("writeMsg:%s", msg);
    int open_USB = open(File_open_USB, O_RDWR);
    if (open_USB < 0)
    {
        return -1;
    }
    char buf[msg.length() + 1];
    strcpy(buf, msg.c_str());
    // 2.串口初始化
    serial_port_init(open_USB);
    write(open_USB, buf, strlen(buf));
    memset(buf, 0, sizeof(buf));
    read(open_USB, buf, sizeof(buf) - 1);
    // printf("接受的数据是:%s\n", buf);
    // memset(buf, 0, sizeof(buf));
    return *buf;
}

/**************************
 * 函数名：serial_port_init
 * 功能：串口初始化
 * 参数：fd：文件描述符
 * 返回值：无
 * ************************/
void serial_port_init(int fd)
{
    struct termios serial_port;
    tcgetattr(fd, &serial_port);
    serial_port.c_cflag |= (CLOCAL | CREAD); /*input mode flag:ignore modem
                                          control lines; Enable receiver */
    serial_port.c_cflag &= ~CSIZE;
    serial_port.c_cflag &= ~CRTSCTS;
    serial_port.c_cflag |= CS8;
    serial_port.c_cflag &= ~CSTOPB; //停止位
    serial_port.c_iflag |= IGNPAR;  // 忽略校验错误
    serial_port.c_oflag = 0;        // 无输出模式
    serial_port.c_lflag = 0;        //本地模式禁用
    cfsetispeed(&serial_port, B115200);
    cfsetospeed(&serial_port, B115200);
    tcsetattr(fd, TCSANOW, &serial_port);
}

// https://blog.csdn.net/persist_with/article/details/118697646
#include "../include/serial.h"
// 打开串口
int serial_open(serial_t *serial, char *devname, long baudrate, char *conf)
{
    printf("aaaa-%d",1222111);

//     int retval;
//     char Baudrate[32];
//     struct termios Newtermios;

//     memset(Baudrate, 0, sizeof(baudrate));
//     memset(&Newtermios, 0, sizeof(struct termios));
//     memset(&(serial->OldTermios), 0, sizeof(struct termios));

//     if (strlen(serial->SerialName) == 0 || devname == NULL)
//     {

//         printf("open_serial Invalid parameter\n");
//         return -1;
//     }

//     if (devname != NULL)
//     {

//         strncpy(serial->SerialName, devname, SERIALNAME_LEN);
//     }
//     else
//     {
//         return -2;
//     }

//     if (baudrate)
//     {
//         serial->Baudrate = baudrate;
//     }
//     else
//     {

//         serial->Baudrate = 9600;
//     }

//     if (conf == NULL)
//     {

//         serial->Databits = 8;
//         serial->Parity = 'N';
//         serial->Stopbits = 1;
//     }
//     else
//     {

//         serial->Databits = atoi(&conf[0]);
//         serial->Parity = conf[1];
//         serial->Stopbits = atoi(&conf[2]);
//     }

//     /*
//      *
//      *  O_RDWR  读写
//      *  O_NOCTTY  如果打开的文件为终端机设备时, 则不会将该终端机当成进程控制终端机.
//      *  O_NONBLOCK 以不可阻断的方式打开文件, 也就是无论有无数据读取或等待, 都会立即返回进程之中.
//      *
//      */

//     serial->fd = open(serial->SerialName, O_RDWR | O_NOCTTY | O_NONBLOCK);

//     if (serial->fd < 0)
//     {

//         printf("%s serail open failed: %s\n", serial->SerialName, strerror(errno));
//         return -3;
//     }

//     if ((retval = fcntl(serial->fd, F_SETFL, 0)) < 0)
//     {
//         printf("%s,Fcntl check faile.  \n", serial->SerialName);
//         return -4;
//     }

//     /* isattr(int fd) 检测设备fd是否是终端，返回1是，0就不是 */

//     if (isatty(serial->fd) == 0)
//     {

//         printf("%s isn`t a device type\n", serial->SerialName);
//         return -5;
//     }

//     printf("%s is a device type \n", serial->SerialName);

//     if (serial == NULL)
//     {

//         printf("Invalid parameter.\n");
//         return -6;
//     }

//     serial->mSend = 128;

//     /*Serial port configuration backup*/
//     if (tcgetattr(serial->fd, &(serial->OldTermios)) != 0)
//     {

//         printf("Serial port configuration backup errno\n");
//         return -7;
//     }

//     if (tcgetattr(serial->fd, &Newtermios))
//     {
//         printf("Get termios to Newtermios failure:%s\n", strerror(errno));
//         return -8;
//     }

//     /* 修改控制模式，保证程序不会占用串口 */
//     Newtermios.c_cflag |= CLOCAL;

//     /* 启动接收器，能够从串口中读取输入数据 */
//     Newtermios.c_cflag |= CREAD;

//     /*  CSIZE字符大小掩码，将与设置databits相关的标致位置零 */
//     Newtermios.c_cflag &= ~CSIZE;

//     Newtermios.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
//     /*
//      * ICANON: 标准模式
//      * ECHO: 回显所输入的字符
//      * ECHOE: 如果同时设置了ICANON标志，ERASE字符删除前一个所输入的字符，WERASE删除前一个输入的单词
//      * ISIG: 当接收到INTR/QUIT/SUSP/DSUSP字符，生成一个相应的信号

// */

//     Newtermios.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
//     /*
//      * BRKINT: BREAK将会丢弃输入和输出队列中的数据(flush)，并且如果终端为前台进程组的控制终端，则BREAK将会产生一个
//      SIGINT信号发送到这个前台进程组
//      * ICRNL: 将输入中的CR转换为NL
//      * INPCK: 允许奇偶校验
//      * ISTRIP: 剥离第8个bits
//      * IXON: 允许输出端的XON/XOF流控

// */

//     /* OPOST: 表示处理后输出，按照原始数据输出 */
//     Newtermios.c_oflag &= ~(OPOST);

//     /* 波特率的设置 */
//     if (serial->Baudrate != 0)
//     {

//         snprintf(Baudrate, sizeof(Baudrate), "B%d", serial->Baudrate);
//         cfsetispeed(&Newtermios, (int)baudrate); //输入
//         cfsetospeed(&Newtermios, (int)baudrate); //输出
//     }
//     else
//     {
//         cfsetispeed(&Newtermios, B9600);
//         cfsetospeed(&Newtermios, B9600);
//     }

//     /* 设置数据位位数 */
//     //字符长度，取值范围为CS5、CS6、CS7或CS8
//     switch (serial->Databits)
//     {

//     case 5:
//         Newtermios.c_cflag |= CS5;
//         break;
//     case 6:
//         Newtermios.c_cflag |= CS6;
//         break;
//     case 7:
//         Newtermios.c_cflag |= CS7;
//         break;
//     case 8:
//         Newtermios.c_cflag |= CS8;
//         break;
//     default:
//         Newtermios.c_cflag |= CS8;
//         break;
//     }

//     /* 设置校验方式 */
//     switch (serial->Parity)
//     {
//     /* 无校验 */
//     case 'n':
//     case 'N':
//         Newtermios.c_cflag &= ~PARENB;
//         Newtermios.c_iflag &= ~INPCK;
//         break;

//         /* 偶校验 */
//     case 'e':
//     case 'E':
//         Newtermios.c_cflag |= PARENB;
//         Newtermios.c_cflag &= ~PARODD;
//         Newtermios.c_iflag |= INPCK;
//         break;

//         /* 奇校验 */
//     case 'o':
//     case 'O':
//         Newtermios.c_cflag |= PARENB;
//         Newtermios.c_cflag |= PARODD;
//         Newtermios.c_iflag |= INPCK;
//         break;

//         /* 默认无校验 */
//     default:
//         Newtermios.c_cflag &= ~PARENB;
//         Newtermios.c_iflag &= ~INPCK;
//         break;
//     }

//     /* 设置停止位 */
//     switch (serial->Stopbits)
//     {
//     case 2:
//         Newtermios.c_cflag |= CSTOPB; //设置两个停止位
//         break;
//     default:
//         Newtermios.c_cflag &= ~CSTOPB; //停止位为1，则要清楚CSTOPB
//         break;
//     }

//     Newtermios.c_cc[VTIME] = 0; //最长等待时间
//     Newtermios.c_cc[VMIN] = 0;  //最小接收字符

//     if (tcflush(serial->fd, TCIFLUSH))
//     {
//         printf("Failed to clear the cache: %s\n", strerror(errno));
//         return -9;
//     }

//     if (tcsetattr(serial->fd, TCSANOW, &Newtermios) != 0)
//     {

//         printf("Serial configuration failure:%s\n", strerror(errno));
//         return -1;
//     }

//     printf("Serial Init Successdully...\n");

//     return serial->fd;
}

int serial_close(serial_t *serial)
{

    int tcs;

    if (!serial)
    {

        printf("close_serial Invalid parameter\n");
        return -1;
    }

    /* 清空终端未完成的数据输入/输出请求数据 */
    if (tcflush(serial->fd, TCIOFLUSH != 0))
    {

        printf("The input and output queues have been flushed failure: %s\n", strerror(errno));
        return -1;
    }
    printf("The input and output queues have been flushed\n");

    tcs = tcsetattr(serial->fd, TCSAFLUSH, &(serial->OldTermios));
    if (tcs != 0)
    {

        printf("%s serial set old options failed: %s\n", serial->SerialName, strerror(errno));
        return -2;
    }

    close(serial->fd);

    return 0;
}

int serial_send(serial_t *serial, char *sbuf, int sbuf_len)
{
    char *ptr, *end;
    int retval;

    if (!serial || !sbuf || sbuf_len <= 0)
    {
        printf("Invalid parameter.\n");
        return -1;
    }

    if (sbuf_len > serial->mSend)
    {
        ptr = sbuf;
        end = sbuf + sbuf_len;

        do
        {
            if (serial->mSend < (end - ptr))
            {
                retval = write(serial->fd, ptr, serial->mSend);
                if (retval <= 0 || retval != serial->mSend)
                {
                    printf("Write to com port[%d] failed:%s\n", serial->fd, strerror(errno));
                    return -2;
                }

                ptr += serial->mSend;
            }
            else
            {
                retval = write(serial->fd, ptr, (end - ptr));
                if (retval <= 0 || retval != (end - ptr))
                {
                    printf("Write to com port[%d] failed:%s\n", serial->fd, strerror(errno));
                    return -3;
                }

                ptr += (end - ptr);
            }
        } while (end > ptr);
    }

    else
    {
        retval = write(serial->fd, sbuf, sbuf_len);
        if (retval <= 0 || retval != sbuf_len)
        {
            printf("Write to com port[[%d] failed:%s\n", serial->fd, strerror(errno));
            return -4;
        }
    }

    return retval;
}

int serial_recv(int fd, char *rbuf, int rbuf_len, int timeout)
{
    cout << "serial_recv" << endl;
    int retval;
    fd_set rset;
    struct timeval time_out;

    if (!rbuf || rbuf_len <= 0)
    {
        printf("serial_recv Invalid parameter.\n");
        return -1;
    }

    if (timeout) //指定延时等待
    {
        time_out.tv_sec = (time_t)(timeout / 1000);
        time_out.tv_usec = 0;

        FD_ZERO(&rset);
        FD_SET(fd, &rset);

        retval = select(fd + 1, &rset, NULL, NULL, &time_out);
        if (retval < 0)
        {
            printf("%s,Select failed:%s\n", strerror(errno));
            return -2;
        }

        else if (0 == retval)
        {
            printf("Time Out.\n");
            return 0;
        }
    }

    usleep(1000);

    retval = read(fd, rbuf, rbuf_len);
    if (retval <= 0)
    {
        printf("Read failed:%s\n", strerror(errno));
        return -3;
    }

    return retval;
}

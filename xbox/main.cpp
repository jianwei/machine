#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <iostream>
#define BAUDRATE B9600		  /// Baud rate : 115200
#define DEVICE "/dev/ttyACM0" // Set your port number

using namespace std;
int nFd = 0;
struct termios stNew;
struct termios stOld;

int SerialInit()
{
	nFd = open(DEVICE, O_RDWR | O_NOCTTY | O_NDELAY);
	if (-1 == nFd)
	{
		perror("Open Serial Port Error!\n");
		return -1;
	}

	if ((fcntl(nFd, F_SETFL, 0)) < 0)
	{
		perror("Fcntl F_SETFL Error!\n");
		return -1;
	}
	if (tcgetattr(nFd, &stOld) != 0)
	{
		perror("tcgetattr error!\n");
		return -1;
	}

	stNew = stOld;
	cfmakeraw(&stNew); // Set the terminal to raw mode, in which all input data is processed in bytes

	// set speed
	cfsetispeed(&stNew, BAUDRATE); // 115200
	cfsetospeed(&stNew, BAUDRATE);
	// set databits
	stNew.c_cflag |= (CLOCAL | CREAD);
	stNew.c_cflag &= ~CSIZE;
	stNew.c_cflag |= CS8;
	// set parity
	stNew.c_cflag &= ~PARENB;
	stNew.c_iflag &= ~INPCK;
	// set stopbits
	stNew.c_cflag &= ~CSTOPB;
	stNew.c_cc[VTIME] = 0; // Specify the minimum number of characters to be read
	stNew.c_cc[VMIN] = 1;  // Specify the waiting time for reading the first character, the unit of time is n*100ms
	// Assuming VTIME=0 is set, the read() operation is blocked indefinitely when no character is input
	tcflush(nFd, TCIFLUSH); // Clear the terminal's unfinished input/output requests and data.
	if (tcsetattr(nFd, TCSANOW, &stNew) != 0)
	{
		perror("tcsetattr Error!\n");
		return -1;
	}
	return nFd;
}

void split(char *src, const char *separator, char **dest, int *num)
{
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
	pNext = strtok(src, separator);
	while (pNext != NULL)
	{
		//存入到目的字符串数组中
		*dest++ = pNext;
		++count;
		/*
			strtok()用来将字符串分割成一个个片段。参数s指向欲分割的字符串，参数delim则为分割字符串中包含的所有字符。
			当strtok()在参数s的字符串中发现参数delim中包涵的分割字符时,则会将该字符改为\0 字符。
			在第一次调用时，strtok()必需给予参数s字符串，往后的调用则将参数s设置成NULL。
			每次调用成功则返回指向被分割出片段的指针。

		*/
		pNext = strtok(NULL, separator);
	}
	*num = count;
}

int main(int argc, char **argv)
{
	int i;
	int nRet = 0;
	char *sendmsg = "MF 40.";
	char buf[5];
	if (SerialInit() == -1)
	{
		perror("SerialInit Error!\n");
		return -1;
	}
	bzero(buf, CSIZE);
	write(nFd, sendmsg, sizeof(sendmsg)); // Send data to serial port
	printf("%s\n", sendmsg);
	char ret[1024] = "";
	while (1)
	{
		// sleep(1);
		/* serial port receiving part*/
		nRet = read(nFd, buf, CSIZE);
		if (-1 == nRet)
		{
			perror("Read Data Error!\n");
			break;
		}
		if (0 < nRet)
		{
			buf[nRet] = 0;
			sprintf(ret, "%s%s", ret, buf);

			// char **data_;
			// int data_len;
			// split_line(ret, &data_, &data_len);
			// char str[100] = "find\nthe\nway";
			char *p[8] = {0};
			int num = 0, i;
			// gets(str);
			// attention!!!!! 这里的分隔符已定要写为字符串的形式。
			

			cout << "------------------------------------begin---------------------------------------" << endl;
			printf("Recv Data: %s\n", ret);
			split(ret, "\n", p, &num);
			cout << "ret:" << ret << endl;
			cout << "data_len:" << p[num-1] << endl;
			cout << "------------------------------------end---------------------------------------" << endl;
		}
	}
	close(nFd);
	return 0;
}
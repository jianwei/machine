#include <stdio.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>

int main(void)
{
	int fd; /*File Descriptor*/

	printf("\n +----------------------------------+");
	printf("\n |        Serial Port Write         |");
	printf("\n +----------------------------------+");

	fd = open("/dev/ttyACM0", O_RDWR | O_NOCTTY | O_NDELAY);

	if (fd == -1) /* Error Checking */
		printf("\n  Error! in Opening ttyACM0  ");
	else
		printf("\n  ttyACM0 Opened Successfully ");

	struct termios SerialPortSettings;

	tcgetattr(fd, &SerialPortSettings);

	//设置波特率
	cfsetispeed(&SerialPortSettings, B9600);
	cfsetospeed(&SerialPortSettings, B9600);

	//设置没有校验
	SerialPortSettings.c_cflag &= ~PARENB;

	//停止位 = 1
	SerialPortSettings.c_cflag &= ~CSTOPB;
	SerialPortSettings.c_cflag &= ~CSIZE;

	//设置数据位 = 8
	SerialPortSettings.c_cflag |= CS8;

	SerialPortSettings.c_cflag &= ~CRTSCTS;
	SerialPortSettings.c_cflag |= CREAD | CLOCAL;

	//关闭软件流动控制
	SerialPortSettings.c_iflag &= ~(IXON | IXOFF | IXANY);

	//设置操作模式
	SerialPortSettings.c_iflag &= ~(ICANON | ECHO | ECHOE | ISIG);

	SerialPortSettings.c_oflag &= ~OPOST;

	if ((tcsetattr(fd, TCSANOW, &SerialPortSettings)) != 0)
		printf("\n  ERROR ! in Setting attributes");
	else
		printf("\n  BaudRate = 9600 \n  StopBits = 1 \n  Parity   = none");

	//定义传输内容
	char write_buffer[] = "MF 40.";
	//传输字节数
	int bytes_written = 0;

	//串口写数据
	bytes_written = write(fd, write_buffer, sizeof(write_buffer));
	printf("\n  %s written to ttyACM0", write_buffer);
	printf("\n  %d Bytes written to ttyACM0", bytes_written);
	printf("\n +----------------------------------+\n\n");

	close(fd);
	return 0;
}

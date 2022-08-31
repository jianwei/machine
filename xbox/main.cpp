#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#define BAUDRATE B9600		  /// Baud rate : 115200
#define DEVICE "/dev/ttyACM0" // Set your port number

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
int main(int argc, char **argv)
{
	int i;
	int nRet = 0;
	char *sendmsg = "MF 40.";
	char buf[50];
	if (SerialInit() == -1)
	{
		perror("SerialInit Error!\n");
		return -1;
	}
	bzero(buf, CSIZE);
	write(nFd, sendmsg, sizeof(sendmsg)); // Send data to serial port
	printf("%s\n", sendmsg);
	// char* ret ="";
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
			// ret = ret + buf
			printf("Recv Data: %s\n", buf);
		}
	}
	close(nFd);
	return 0;
}
#include "./include/serial.h"
#include <stdio.h>
#include <string.h>
// #include <iostream>

// using namespace std;

int main()
{

    serial_t serial;
    char conf;
    char *sbuf;
    char *rbuf;
    int sbuf_len = 8;
    int rbuf_len = 8;
    int timeout = 3600;
    serial_open(&serial, "/dev/ttyAMA0", 9600, &conf);
    // serial_send(&serial, &sbuf, sbuf_len);

    // serial_recv(serial.fd, &rbuf, rbuf_len, timeout);
    // serial_close(&serial);
    // cout << "iiii" << endl;
    // printf("a%d", 1);
    // int a = 111111;
    // printf("%d", a);

    return 0;
}

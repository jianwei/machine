#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <linux/input.h>
#include <linux/joystick.h>
#include <iostream>
#include <math.h>
// #include "./seria.cpp"

#define XBOX_TYPE_BUTTON 0x01
#define XBOX_TYPE_AXIS 0x02

#define XBOX_BUTTON_A 0x00
#define XBOX_BUTTON_B 0x01
#define XBOX_BUTTON_X 0x02
#define XBOX_BUTTON_Y 0x03
#define XBOX_BUTTON_LB 0x04
#define XBOX_BUTTON_RB 0x05
#define XBOX_BUTTON_START 0x06
#define XBOX_BUTTON_BACK 0x07
#define XBOX_BUTTON_HOME 0x08
#define XBOX_BUTTON_LO 0x09 /* 左摇杆按键 */
#define XBOX_BUTTON_RO 0x0a /* 右摇杆按键 */

#define XBOX_BUTTON_ON 0x01
#define XBOX_BUTTON_OFF 0x00

#define XBOX_AXIS_LX 0x00 /* 左摇杆X轴 */
#define XBOX_AXIS_LY 0x01 /* 左摇杆Y轴 */
#define XBOX_AXIS_RX 0x03 /* 右摇杆X轴 */
#define XBOX_AXIS_RY 0x04 /* 右摇杆Y轴 */
#define XBOX_AXIS_LT 0x02
#define XBOX_AXIS_RT 0x05
#define XBOX_AXIS_XX 0x06 /* 方向键X轴 */
#define XBOX_AXIS_YY 0x07 /* 方向键Y轴 */

#define XBOX_AXIS_VAL_UP -32767
#define XBOX_AXIS_VAL_DOWN 32767
#define XBOX_AXIS_VAL_LEFT -32767
#define XBOX_AXIS_VAL_RIGHT 32767

#define XBOX_AXIS_VAL_MIN -32767
#define XBOX_AXIS_VAL_MAX 32767
#define XBOX_AXIS_VAL_MID 0x00

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

double global_max = 32767;
char global_pwd[80] = "";
// char writeMsg(string msg);

int xbox_open(const char *file_name)
{
    int xbox_fd;

    xbox_fd = open(file_name, O_RDONLY);
    if (xbox_fd < 0)
    {
        perror("open");
        return -1;
    }

    return xbox_fd;
}

int xbox_map_read(int xbox_fd, xbox_map_t *map)
{
    int len, type, number, value;
    struct js_event js;

    len = read(xbox_fd, &js, sizeof(struct js_event));
    if (len < 0)
    {
        perror("read");
        return -1;
    }

    type = js.type;
    number = js.number;
    value = js.value;

    map->time = js.time;
    // cout << "type:" << type << endl;
    // cout << "number:" << number << endl;
    if (type == JS_EVENT_BUTTON)
    {
        switch (number)
        {
        case XBOX_BUTTON_A:
            map->a = value;
            break;

        case XBOX_BUTTON_B:
            map->b = value;
            break;

        case XBOX_BUTTON_X:
            map->x = value;
            break;

        case XBOX_BUTTON_Y:
            map->y = value;
            break;

        case XBOX_BUTTON_LB:
            map->lb = value;
            break;

        case XBOX_BUTTON_RB:
            map->rb = value;
            break;

        case XBOX_BUTTON_START:
            map->start = value;
            break;

        case XBOX_BUTTON_BACK:
            map->back = value;
            break;

        case XBOX_BUTTON_HOME:
            map->home = value;
            break;

        case XBOX_BUTTON_LO:
            map->lo = value;
            break;

        case XBOX_BUTTON_RO:
            map->ro = value;
            break;

        default:
            break;
        }
    }
    else if (type == JS_EVENT_AXIS)
    {
        switch (number)
        {
        case XBOX_AXIS_LX:
            map->lx = value;
            break;

        case XBOX_AXIS_LY:
            map->ly = value;
            break;

        case XBOX_AXIS_RX:
            map->rx = value;
            break;

        case XBOX_AXIS_RY:
            map->ry = value;
            break;

        case XBOX_AXIS_LT:
            map->lt = value;
            break;

        case XBOX_AXIS_RT:
            map->rt = value;
            break;

        case XBOX_AXIS_XX:
            map->xx = value;
            break;

        case XBOX_AXIS_YY:
            map->yy = value;
            break;

        default:
            break;
        }
    }
    else
    {
        /* Init do nothing */
    }

    return len;
}

void xbox_close(int xbox_fd)
{
    close(xbox_fd);
    return;
}





void exec_shell(char params[], char* &ret){
    cout<<"exec_shell:"<< params <<endl;
    char* cmd_all;
    if(strlen(global_pwd)==0){
        char buf[80];
        getcwd(buf,sizeof(buf));
        sprintf(global_pwd, "%s",buf);
    }
    cout<<123<<endl;
    sprintf(cmd_all, "cd %s/../center/ &&  python3 scripts.py %s",global_pwd,params);
    cout<< "cmd_all:"<<cmd_all<<endl;
    
    FILE *fp;
    char buffer[80]; 
    return ;
    fp = popen(cmd_all,"r");
    fgets(buffer,sizeof(buffer),fp);
    pclose(fp);
    ret = buffer;
    cout << "script:"<<cmd_all << ",vaule:"<<buffer <<endl;
}



int send_cmd(const char *cmd){
    printf("send_cmd:%s \r\n",cmd);
    string msg =  cmd;
    printf("send_cmd,msg:%s \r\n",msg.c_str());
    // writeMsg(msg.c_str());  
    return 0;
}



void stop (int type){
    string cmd = "stop "+to_string(type);
    send_cmd(cmd.c_str());
}

void go(int ry){
    string direction =  "MF";
    if(ry>0){
        direction = "MB";
    }
    string cmd = "";
    int absry = abs(ry);
    float pre = (absry/global_max) * 100;
    cmd = direction+" "+to_string((int)pre);
    // printf("go:%s,ry:%d,global_max:%f,absry:%d,pre:%f,intpre:%d,cmd:%s \r\n",direction.c_str(),ry,global_max,absry,pre,(int)pre,cmd.c_str());    
    printf("cmd:%s \r\n",cmd.c_str());    
    send_cmd(cmd.c_str());
}



void turn(int x,int y){
    double angle = 0;
    string cmd = "";
    //下面2象限 复原 
    if( (x>0 && y>0) || (x<0 && y>0) ){
        angle = 0;
    }else if (x!=0 && y==0){
        angle = 90;
    }else{
        double xx = abs(x);
        double yy = abs(y);
        if (yy!=0){
            double z = xx/yy;
            angle = atan(z) * 180.0/3.1415926;
        }
    }
    cmd = "TA "+to_string((int)angle);
    send_cmd(cmd.c_str());
}


void left_right(int x){
    if(x!=0){
        string cmd = "";
        if (x>0){
            cmd = "ML 10";
        }else{
            cmd = "MR 10";
        }
        send_cmd(cmd.c_str());
    }
}

void up_down(int y){
    if(y!=0){
        string cmd = "";
        if (y>0){
            cmd = "MU 10";
        }else{
            cmd = "MD 10";
        }
        send_cmd(cmd.c_str());
    }
}




int main(void)
{
    int xbox_fd;
    xbox_map_t map;
    int len, type;
    int axis_value, button_value;
    int number_of_axis, number_of_buttons;
  

    memset(&map, 0, sizeof(xbox_map_t));

    xbox_fd = xbox_open("/dev/input/js1");
    if (xbox_fd < 0)
    {
        return -1;
    }

    while (1)
    {
        len = xbox_map_read(xbox_fd, &map);
        if (len < 0)
        {
            usleep(10 * 1000);
            continue;
        }
        // printf("\rTime:%8d A:%d B:%d X:%d Y:%d LB:%d RB:%d start:%d back:%d home:%d LO:%d RO:%d XX:%-6d YY:%-6d LX:%-6d LY:%-6d RX:%-6d RY:%-6d LT:%-6d RT:%-6d",
        //         map.time, map.a, map.b, map.x, map.y, map.lb, map.rb, map.start, map.back, map.home, map.lo, map.ro,
        //         map.xx, map.yy, map.lx, map.ly, map.rx, map.ry, map.lt, map.rt);

        // printf("\rTime:%8d  LO:%d RO:%d  LX:%d LY:%d RX:%d RY:%d \r\n", map.time, map.lo, map.ro,map.lx, map.ly, map.rx, map.ry);
        //开始工作、停止工作
        if(map.rb==1){
            char* ret;
            char params[128] = "";

            // string cmd = "echo 1";
            // char cmd[] = "--type 1 --cmd 1";
            // exec_shell(cmd,val);
            sprintf(params,"--type 2 --dict {\\\"%s\\\":%s}","begin_work","1");
            // cout <<10000<< params << endl;

            exec_shell(params,ret);
            // printf("shell--value:%s",val);
        }

        //停车
        if(map.ro==1){
            stop(1);
        }
        //前进 后退
        if(map.ry!=0){
           go(map.ry);
        }
        //转向
        if(map.lx!=0 || map.ly!=0){
            turn(map.lx,map.ly);
        }
        // 上下
        if( map.yy!=0){
            up_down(map.yy);
        }
        // 左右
        if(map.xx!=0 ){
            left_right(map.xx);
        }

        fflush(stdout);
    }

    xbox_close(xbox_fd);
    return 0;
}

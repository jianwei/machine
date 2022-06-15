#include "rclcpp/rclcpp.hpp"

/*
    创建一个类节点，名字叫做itofNode,继承自Node.
*/
class itofNode : public rclcpp::Node
{

public:
    // 构造函数,有一个参数为节点名称
    itofNode(std::string name) : Node(name)
    {
        // 打印一句自我介绍
        RCLCPP_INFO(this->get_logger(), "node:%s.",name.c_str());
    }

   
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    /*产生一个itofNode的节点*/
    auto node = std::make_shared<itofNode>("itof");
    /* 运行节点，并检测退出信号*/
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
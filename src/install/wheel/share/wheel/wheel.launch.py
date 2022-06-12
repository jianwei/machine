# 导入库
from launch import LaunchDescription
from launch_ros.actions import Node

# 定义函数名称为：generate_launch_description
def generate_launch_description():
    # 创建Actions.Node对象li_node，标明李四所在位置
    wheel_node_go = Node(
        package="wheel",
        executable="wheel_node_go"
        )
    # 创建Actions.Node对象wang2_node，标明王二所在位置
    wheel_node_stop = Node(
        package="wheel",
        executable="wheel_node_stop"
        )
    # 创建LaunchDescription对象launch_description,用于描述launch文件
    launch_description = LaunchDescription([wheel_node_go,wheel_node_stop])
    # 返回让ROS2根据launch描述执行节点
    return launch_description
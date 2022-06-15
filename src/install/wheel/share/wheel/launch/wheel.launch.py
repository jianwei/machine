# 导入库
from launch import LaunchDescription
from launch_ros.actions import Node

# 定义函数名称为：generate_launch_description
def generate_launch_description():
    wheel_node_go = Node(
        package="wheel",
        executable="wheel_node_go"
        )
    wheel_node_stop = Node(
        package="wheel",
        executable="wheel_node_stop"
        )
    launch_description = LaunchDescription([wheel_node_go,wheel_node_stop])
    return launch_description
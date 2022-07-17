# 导入库
from launch import LaunchDescription
from launch_ros.actions import Node

# 定义函数名称为：generate_launch_description
def generate_launch_description():
    weeding_node = Node(
        package="weeding",
        executable="weeding_node"
        )
    camera_node = Node(
        package="weeding",
        executable="camera_node"
        )        
    launch_description = LaunchDescription([weeding_node,camera_node])
    return launch_description
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Path to your URDF file
    # Ensure you've placed scungun.urdf in a 'urdf' folder in your package
    pkg_share = get_package_share_directory('IMU_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'IMU.urdf')

    with open(urdf_file, 'r') as infp:
        robot_description_config = infp.read()

    return LaunchDescription([
        # 2. Robot State Publisher (The TF "thingy")
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_config}]
        ),

        # 3. Your IMU Driver
        Node(
            package='IMU_driver',
            executable='driver_node.py',  # Or the name of your C++ executable
            name='scungun_driver',
            output='screen',
        ),
        
        # 4. Optional: Static Transform for the whole box to the world
        # This keeps the box from "flying away" in RViz if you don't have a map yet
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments = ['0', '0', '0', '0', '0', '0', 'world', 'imu_box_base']
        )
    ])
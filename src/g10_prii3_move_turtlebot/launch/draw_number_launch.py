import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    set_turtlebot_model = SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger')

    gazebo_launch_dir = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'), 'launch'
    )

    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_launch_dir, 'empty_world.launch.py')
        )
    )

    run_draw_number_node = Node(
        package='g10_prii3_move_turtlebot',
        executable='draw_number',
        name='draw_number_node',
        output='screen'
    )

    return LaunchDescription([
        set_turtlebot_model,
        launch_gazebo,
        run_draw_number_node
    ])

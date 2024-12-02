from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    
    remap_number_topic = ("number", "my_number")
    
    number_publisher_node = Node(
        package='my_py_pkg',
        executable='number_publisher',
        name='maiyn_number_publisher',
        remappings=[
            remap_number_topic
        ],
        parameters=[
            {"number_to_publish": 5},
            {"publish_frequency": 7.0}
        ]
    )
    
    counter_node = Node(
        package='my_py_pkg',
        executable='number_counter',
        name='main_number_counter',
        remappings=[
            remap_number_topic,
            ("number_count", "my_number_count")
        ]
    )
     
    
    ld.add_action(counter_node)
    ld.add_action(number_publisher_node)
    return ld
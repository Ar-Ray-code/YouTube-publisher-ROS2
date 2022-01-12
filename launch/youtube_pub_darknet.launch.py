import launch
import launch_ros.actions
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from youtube_publisher.youtube_pub import youtube_publisher

def generate_launch_description():
    youtube_publisher_share_dir = get_package_share_directory('youtube_publisher')

    darknet_ros_share_dir = get_package_share_directory('darknet_ros')
    network_param_file = darknet_ros_share_dir + '/config/yolov4-tiny.yaml'

    youtube = launch_ros.actions.Node(
        package='youtube_publisher', executable='youtube_pub',
        parameters=[
            {'topic_name': '/image_raw'},
            {'cache_path': youtube_publisher_share_dir + '/cache'},
            {'video_url' : 'https://youtu.be/CFLOiR2EbKM'},
            {'using_youtube_dl' : True},
            {'clear_cache_force' : False},
            {'width' : 854},
            {'height' : 480},
            {'speed' : 1.0},
            {'imshow_is_show' : False}
        ],
    )

    darknet_ros_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([darknet_ros_share_dir + '/launch/darknet_ros.launch.py']),
      launch_arguments={'network_param_file': network_param_file}.items()
  )

    return launch.LaunchDescription([
        youtube,
        darknet_ros_launch,
    ])
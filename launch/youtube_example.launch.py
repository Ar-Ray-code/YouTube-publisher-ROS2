import launch
import launch_ros.actions
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from youtube_publisher.youtube_pub import youtube_publisher

def generate_launch_description():
    # yolox_ros_share_dir = get_package_share_directory('yolox_ros_py')
    youtube_publisher_share_dir = get_package_share_directory('youtube_publisher')

    youtube = launch_ros.actions.Node(
        package="youtube_publisher", executable="youtube_pub",
        parameters=[
            {"topic_name": "/image_raw"},
            {'cache_path': youtube_publisher_share_dir + '/cache'},
            {"video_url" : "https://www.youtube.com/watch?v=Cf7VdXwjUIE"},
            {"using_youtube_dl" : True},
            {"clear_cache_force" : False},
            {"width" : 720},
            {"height" : 480},
        ],
    )

    # yolox_ros = launch_ros.actions.Node(
    #     package="yolox_ros_py", executable="yolox_ros",
    #     parameters=[
    #         {"image_size/width": 640},
    #         {"image_size/height": 480},
    #         {"yolo_type" : 'yolox-l'},
    #         {"fuse" : False},
    #         {"trt" : False},
    #         {"rank" : 0},
    #         {"ckpt_file" : yolox_ros_share_dir+"/yolox_l.pth"},
    #         {"conf" : 0.3},
    #         {"nmsthre" : 0.65},
    #         {"img_size" : 640},
    #     ],
    # )

    rqt_graph = launch_ros.actions.Node(
        package="rqt_graph", executable="rqt_graph",
    )

    return launch.LaunchDescription([
        youtube
    ])
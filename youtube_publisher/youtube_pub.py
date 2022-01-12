# using https://youtu.be/Cf7VdXwjUIE

from __future__ import unicode_literals
import youtube_dl
import cv2
import numpy as np

import os
import ffmpeg

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class youtube_publisher(Node):
    def __init__(self):
        super().__init__('youtube_publisher')
        # param
        self.declare_parameter('topic_name', 'image')
        self.declare_parameter('cache_path', '~/cache/youtube_publisher')
        self.declare_parameter('video_url', 'https://www.youtube.com/watch?v=Cf7VdXwjUIE')
        self.declare_parameter('using_youtube_dl', True)
        self.declare_parameter('clear_cache_force', False)
        self.declare_parameter('cache_file_name', 'data')
        self.declare_parameter('imshow_is_show', True)
        self.declare_parameter('width', 720)
        self.declare_parameter('height', 480)

        topic_name = self.get_parameter('topic_name').value
        cache_path = self.get_parameter('cache_path').value.replace('~', os.environ['HOME'])
        video_url = self.get_parameter('video_url').value
        using_youtube_dl = self.get_parameter('using_youtube_dl').value
        clear_cache_force = self.get_parameter('clear_cache_force').value # true or false
        cache_file_name = self.get_parameter('cache_file_name').value

        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value
        self.imshow_is_show = self.get_parameter('imshow_is_show').value
        
        ydl_opts = {}

        if clear_cache_force:
            os.system('rm -rf ' + cache_path)
            self.create_folder_and_cd(cache_path)
        
        if os.path.exists(cache_path + '/url.txt'):
            with open(cache_path + '/url.txt', 'r') as f:
                url = f.readline()
        
                if url == video_url:
                    print('use cache. youtube_dl not used.')
                    using_youtube_dl = False
                else:
                    print('cache not found. youtube_dl will be used.')
                    f.close()
                    os.system('rm -rf ' + cache_path)
                    self.create_folder_and_cd(cache_path)
            
        if using_youtube_dl:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                self.create_folder_and_cd(cache_path)
                ydl.download([video_url])

                # text file for check same video
                with open(cache_path + '/url.txt', 'w') as f:
                    f.write(video_url)
        
            os.system("mv " + cache_path + "/*.mkv " + cache_path + "/" + cache_file_name + ".mkv")
            stream = ffmpeg.input(cache_path + "/" + cache_file_name + ".mkv").output(cache_path + "/" + cache_file_name + ".avi", vcodec='libx264', pix_fmt='yuv420p', r='30')
            ffmpeg.run(stream)
            os.system("rm -rf " + cache_path + "/" + cache_file_name + ".mkv")
        
        # Open Video file ===============================================
        self.cap = cv2.VideoCapture(cache_path + "/" + cache_file_name + ".avi")
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # publisher
        self.publisher = self.create_publisher(Image, topic_name, 10)
        self.bridge = CvBridge()

        # timer
        self.timer_period = 1.0 / fps
        self.timer = self.create_timer(self.timer_period, self.publish_video)

    def publish_video(self):
        ret, frame = self.cap.read()
        if ret == True:
            try:
                resized = cv2.resize(frame, (self.width, self.height))
                msg = self.bridge.cv2_to_imgmsg(resized, encoding="bgr8")
                msg.header.frame_id = "camera"
                self.publisher.publish(msg)
                # cap open
                if self.imshow_is_show:
                    cv2.imshow('frame', resized)
                    cv2.waitKey(1)
                else:
                    pass
            except CvBridgeError as e:
                print(e)
        else:
            self.timer.cancel()
            self.cap.release()
            cv2.destroyAllWindows()
            self.destroy_node()

    def create_folder_and_cd(self, path):
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

def ros_main(args = None):
    rclpy.init(args=args)

    youtube_publisher_class = youtube_publisher()
    rclpy.spin(youtube_publisher_class)

    youtube_publisher_class.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    ros_main()
# YouTube-publisher-ROS2

## Installation

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/Ar-Ray-code/YouTube-publisher-ROS2.git
pip3 install -r YouTube-publisher-ROS2/requirements.txt
cd ~/ros2_ws
colcon build --symlink-install
```

## Demo with YOLOX-ROS

### Build

```bash
# YOLOX installation
cd ~/Documents/
git clone --recursive https://github.com/Megvii-BaseDetection/YOLOX
cd ~/Documents/YOLOX
pip3 install -U pip && pip3 install -r requirements.txt
pip3 install -v -e .  # or  python3 setup.py develop
pip3 install cython; pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

# ROS2 Installation
cd ~/ros2_ws/src

git clone https://github.com/Ar-Ray-code/YouTube-publisher-ROS2.git
git clone https://github.com/Ar-Ray-code/YOLOX-ROS.git --recursive
pip3 install -r YouTube-publisher-ROS2/requirements.txt

cd ~/ros2_ws
colcon build --symlink-install
```

### Run

```bash
ros2 launch youtube_publisher youtube_publisher_yolox.launch.py
```
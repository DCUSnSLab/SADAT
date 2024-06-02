# SADAT(SnS Laboratory Autonomous Driving Analysis Tool)

## Introduction

This tool helps to analysis and re-simulate autonomous driving techs which are sensor physics&theory, object tracking&estimation, path planing and so on.

## Requirements
SADAT requires the following libraries:
- pyqt5
- pyqtgraph
- vispy
- rospy(if you use rospackage)

The following ROS packages are required:
- rosnumpy
- zed-ros-interfaces([link](https://github.com/stereolabs/zed-ros-interfaces))

## Preinstallation
rosnumpy
```
  $ sudo apt-get install ros-$release-ros-numpy
```

zed-ros-interface
```
  $ cd ~/catkin_ws/src
  $ git clone https://github.com/stereolabs/zed-ros-interfaces.git
  $ cd ../
  $ rosdep install --from-paths src --ignore-src -r -y
  $ catkin_make -DCMAKE_BUILD_TYPE=Release
  $ source ./devel/setup.bash
```

## Python dependency installation (Do not use requirements.txt file)
```
pip install vispy
pip install opencv-python-headless
pip install pyqt5==5.14.2
pip install serial
pip install pyqtgraph==0.12.1
pip install rospkg==1.2.9
```
Pycharm을 통해 실행할 때
File - Settings - Project: - Project Structure 항목에서
Content Root 경로에 ROS Python 패키지 경로를 추가해줘야함
/opt/ros/(ROS distro)/lib/python3/dist-packages

## Version Information
- v0.2 : [SADAT v0.2](http://itgit.cu.ac.kr/AutonomousDriving/SADAT/post/5)
- v0.1

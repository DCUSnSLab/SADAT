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

## Version Information
- v0.2 : [SADAT v0.2](http://itgit.cu.ac.kr/AutonomousDriving/SADAT/post/5)
- v0.1

cmake_minimum_required(VERSION 2.8.3)
project(dynamic_rviz_config)

find_package(catkin REQUIRED COMPONENTS
  rospy
  rviz
)

catkin_python_setup()
catkin_package(
  LIBRARIES dynamic_rviz_config
  CATKIN_DEPENDS rospy rviz
  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)


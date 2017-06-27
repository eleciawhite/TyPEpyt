# Install script for directory: /home/nvidia/Ty/TyPEpyt/ros_ws/src/typepyt

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/nvidia/Ty/TyPEpyt/ros_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt/msg" TYPE FILE FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/src/typepyt/msg/JointAngles.msg")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt/action" TYPE FILE FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/src/typepyt/action/ArmJointAngles.action")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt/msg" TYPE FILE FILES
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesAction.msg"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesActionGoal.msg"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesActionResult.msg"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesActionFeedback.msg"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesGoal.msg"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesResult.msg"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/typepyt/msg/ArmJointAnglesFeedback.msg"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt/cmake" TYPE FILE FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/build/typepyt/catkin_generated/installspace/typepyt-msg-paths.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/include/typepyt")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/roseus/ros/typepyt")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/common-lisp/ros/typepyt")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/share/gennodejs/ros/typepyt")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  execute_process(COMMAND "/usr/bin/python" -m compileall "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/lib/python2.7/dist-packages/typepyt")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/devel/lib/python2.7/dist-packages/typepyt")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/build/typepyt/catkin_generated/installspace/typepyt.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt/cmake" TYPE FILE FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/build/typepyt/catkin_generated/installspace/typepyt-msg-extras.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt/cmake" TYPE FILE FILES
    "/home/nvidia/Ty/TyPEpyt/ros_ws/build/typepyt/catkin_generated/installspace/typepytConfig.cmake"
    "/home/nvidia/Ty/TyPEpyt/ros_ws/build/typepyt/catkin_generated/installspace/typepytConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/typepyt" TYPE FILE FILES "/home/nvidia/Ty/TyPEpyt/ros_ws/src/typepyt/package.xml")
endif()


cmake_minimum_required(VERSION 2.8.3)
project(TOF_01_lidar)

set(TOF_01_LIDAR_SDK_PATH "./src/")

FILE(GLOB TOF_01_LIDAR_SDK_SRC 
  "${TOF_01_LIDAR_SDK_PATH}/src/*.cpp"
)

include_directories(
  ${TOF_01_LIDAR_SDK_PATH}/include
  ${TOF_01_LIDAR_SDK_PATH}/src
)

add_executable(TOF_01_lidar_node app/node.cpp ${TOF_01_LIDAR_SDK_SRC})
target_link_libraries(TOF_01_lidar_node -lrt -lpthread)



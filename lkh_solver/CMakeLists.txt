cmake_minimum_required(VERSION 2.8.3)
project(lkh_solver)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_package(
  CATKIN_DEPENDS
    roscpp
)

include_directories(include)

# Build LKH
file(GLOB LKH_SRC
    "src/*.c"
)
add_executable(${PROJECT_NAME} ${LKH_SRC})
target_link_libraries(${PROJECT_NAME} -lm)

install(
  TARGETS
    ${PROJECT_NAME}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

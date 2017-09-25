cmake_minimum_required(VERSION 2.8.3)
project(lkh_solver)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_python_setup()

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

# Tests
catkin_add_nosetests(tests/test_modules.py)

# Install nodes
install(
  TARGETS
    ${PROJECT_NAME}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Install instances
install(
  DIRECTORY tsplib
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

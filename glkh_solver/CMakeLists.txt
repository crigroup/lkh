cmake_minimum_required(VERSION 2.8.3)
project(glkh_solver)

find_package(catkin REQUIRED COMPONENTS
  lkh_solver
  roscpp
)

catkin_package(
  CATKIN_DEPENDS
    lkh_solver
    roscpp
)
include_directories(include)

# Build libraries
set(COMMON_SRC_FILES
  src/SolveGTSP.c
  src/SolveTSP.c
  src/PostOptimize.c
  src/Distance.c
  src/Distance_SPECIAL.c
  src/eprintf.c
  src/fscanint.c
  src/GetTime.c
  src/IsCandidate.c
  src/printff.c
  src/PrintParameters.c
  src/Random.c
  src/ReadLine.c
  src/ReadParameters.c
  src/ReadPenalties.c
  src/ReadProblem.c
  src/Statistics.c
  src/WriteTour.c
)

# Build nodes
add_executable(glkh_solver src/GLKHmain.c ${COMMON_SRC_FILES})
target_link_libraries(glkh_solver -lm)
add_executable(glkh_exp_solver src/GLKH_EXPmain.c ${COMMON_SRC_FILES})
target_link_libraries(glkh_exp_solver -lm)
add_executable(glkh_check_solver src/GLKH_CHECKmain.c ${COMMON_SRC_FILES})
target_link_libraries(glkh_check_solver -lm)

# Tests
catkin_add_nosetests(tests/test_modules.py)

# Install nodes
install(
  TARGETS
    glkh_solver
    glkh_exp_solver
    glkh_check_solver
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Install instances
install(
  DIRECTORY gtsplib
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

# lkh
ROS packages by [CRI Group](http://www.ntu.edu.sg/home/cuong/),
[Nanyang Technological University, Singapore](http://www.ntu.edu.sg).

The LKH and GLKH solvers have been copied from:
http://webhotel4.ruc.dk/~keld/research/GLKH/

### Maintainer
* [Francisco Suárez Ruiz](http://fsuarez6.github.io)

### Documentation
* Throughout the various files in this repository.
* Website: http://wiki.ros.org/lkh

## License
These packages are distributed under BSD 3-clause license but the LKH and GLKH
software state the following:
> The developed software is free of charge for academic and non-commercial use

## Travis - Continuous Integration

[![Build Status](https://travis-ci.org/crigroup/lkh.svg?branch=master)](https://travis-ci.org/crigroup/lkh)


## ROS Buildfarm

Package | Kinetic Source | Kinetic Debian
------- | -------------- | --------------
lkh     | [![Build Status](http://build.ros.org/buildStatus/icon?job=Ksrc_uX__lkh__ubuntu_xenial__source)](http://build.ros.org/job/Ksrc_uX__lkh__ubuntu_xenial__source/) | [![Build Status](http://build.ros.org/buildStatus/icon?job=Kbin_uX64__lkh__ubuntu_xenial_amd64__binary)](http://build.ros.org/job/Kbin_uX64__lkh__ubuntu_xenial_amd64__binary/)
lkh_solver | [![Build Status](http://build.ros.org/buildStatus/icon?job=Ksrc_uX__lkh_solver__ubuntu_xenial__source)](http://build.ros.org/job/Ksrc_uX__lkh_solver__ubuntu_xenial__source/) | [![Build Status](http://build.ros.org/buildStatus/icon?job=Kbin_uX64__lkh_solver__ubuntu_xenial_amd64__binary)](http://build.ros.org/job/Kbin_uX64__lkh_solver__ubuntu_xenial_amd64__binary/)
glkh_solver | [![Build Status](http://build.ros.org/buildStatus/icon?job=Ksrc_uX__glkh_solver__ubuntu_xenial__source)](http://build.ros.org/job/Ksrc_uX__glkh_solver__ubuntu_xenial__source/) | [![Build Status](http://build.ros.org/buildStatus/icon?job=Kbin_uX64__glkh_solver__ubuntu_xenial_amd64__binary)](http://build.ros.org/job/Kbin_uX64__glkh_solver__ubuntu_xenial_amd64__binary/)

[Check
here](http://repositories.ros.org/status_page/ros_kinetic_default.html?q=lkh)
which versions of these packages are in **building**, **ros-shadow-fixed**
(tagged as 'testing'), and **ros** (tagged as 'main').

Approximately every two weeks, the ROS platform manager manually synchronizes
the contents of **ros-shadow-fixed** into **ros** (the public repository).

.set GIT=https://github.com/zeromq/zproject
.sub 0MQ=ØMQ

# zproject - Class Project Generator

## Contents

.toc 2

## Overview

zproject is a community project, like most ZeroMQ projects, built using the C4.1 process, and licensed under MPL v2. It solves the Makefile problem really well. It is unashamedly for C, and more pointedly, for that modern C dialect we call CLASS. CLASS is the Minecraft of C: fun, easy, playful, mind-opening, and social. [hintjens#79](http://hintjens.com/blog:79)

### Scope and Goals

zproject has these goals:

* generate files for cross-platform build environments.
* generate public and private headers. 
* generate CLASS (ZeroMQ RFC/21) compliant header and source skeletons for new classes.
* generate CI setup for travis.

zproject grew out of the work that has been done to automatically generate the build environment in CZMQ.

All you need is a project.xml in the project's root directory which is your 

    One file to rule them all

The following build environments are currently supported:
 
* android (not tested)
* autotools (tested)
* cmake (not tested)
* mingw32 (not tested)
* qt-android (tested)
* vs2008 (not tested)
* vs2010 (not tested)
* vs2012 (not tested)
* vs2013 (not tested)
 
All classes in the project.xml are automatically added to all build environments. Further as you add new classes to your project you can generate skeleton header and source files according to [the CLASS RFC](http://rfc.zeromq.org/spec:21).

## Sample configuration

The following snippet is the `project.xml` from zproject:

.pull project.xml, code

## Installation

Before you start you'll need to install the code generator GSL (https://github.com/imatix/gsl) on your system. Then execute the generate.sh script to generate the build environment files for zproject.

    ./generate.sh

After that proceed with your favorite build environment. (Currently only autotools!)

### autotools

The following will install the `zproject-*.gsl` files to `/usr/local/bin` where gsl will find them if you use zproject in your project.

    ./autogen.sh
    ./configure
    make
    make install

## Generate build environment in your project

Copy the `project.xml` and `generate.sh` to your project or an empty directory and adjust the values accordingly.

Run `./generate.sh`

## Ownership and License

The contributors are listed in AUTHORS. This project uses the MPL v2 license, see LICENSE.

zproject uses the [C4.1 (Collective Code Construction Contract)](http://rfc.zeromq.org/spec:22) process for contributions.

To report an issue, use the [zproject issue tracker](https://github.com/zeromq/zproject/issues) at github.com.

## Removal

### autotools

    make uninstall

### Hints to Contributors

Before you commit code please make sure that the project model hides all details of backend scripts.

For example don't make a user enter a header file because autoconf needs it to do AC_CHECK_LIB.

### This Document

This document is originally at README.txt and is built using [gitdown](http://github.com/imatix/gitdown).

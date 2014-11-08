.set GIT=https://github.com/zeromq/zproject
.sub 0MQ=ØMQ

# zproject - rfc/21 project generator

## Contents

.toc 2

## Overview

### Scope and Goals

zproject has these goals:

* generate files for cross-platform build environments.
* generate public and private headers. 
* generate rfc/21 compliant header and source skeletons for new classes
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
 
All classes in the project.xml are automatically added to all build environments. Further as you add new classes to your project you can generate skeleton header and source files according to [rfc/21](http://rfc.zeromq.org/spec:21).

## Sample configuration

The following snippet is the project.xml from zproject with explains all available tags and attributes.

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

## Removal

### autotools

    make uninstall


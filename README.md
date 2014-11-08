
<A name="toc1-3" title="zproject - rfc/21 project generator" />
# zproject - rfc/21 project generator

<A name="toc2-6" title="Contents" />
## Contents


**<a href="#toc2-11">Overview</a>**
&emsp;<a href="#toc3-14">Scope and Goals</a>

**<a href="#toc2-44">Sample configuration</a>**

**<a href="#toc2-159">Installation</a>**
&emsp;<a href="#toc3-168">autotools</a>

**<a href="#toc2-178">Generate build environment in your project</a>**

**<a href="#toc2-185">Removal</a>**
&emsp;<a href="#toc3-188">autotools</a>

<A name="toc2-11" title="Overview" />
## Overview

<A name="toc3-14" title="Scope and Goals" />
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

<A name="toc2-44" title="Sample configuration" />
## Sample configuration

The following snippet is the project.xml from zproject with explains all available tags and attributes.

<!-- 
    The project.xml generates build environments for:

        * android
        * autotool
        * cmake
        * mingw32
        * vs2008
        * vs2010
        * vs2012
        * vs2013

    Classes are automatically added to all build environments. Further as you
    add new classes to your project you can generate skeleton header and source 
    files according to http://rfc.zeromq.org/spec:21.

    name := The name of your project
    description := A short description for your project
    script := The gsl script to generate all the stuff !!! DO NOT CHANGE !!!
    email := The email address where to reach you project e.g. mailinglist.
-->
<project
    name = "myproject"
    description = "My Project that will change the world."
    script = "zproject.gsl"
    email = "mail@myproject.org"
    >

    <!--
        Includes are processed first, so XML in included files will be
        part of the XML tree
    -->
    <include filename = "license.xml" />

    <!-- 
        Current version of your project. 
        This will be used to package your distribution 
    -->
    <version major = "1" minor = "0" patch = "0" />

    <!--
        Specify which other projects this depends on; these projects must be
        known by zproject, and you do not have to specify subdependencies.
        Known projects are zyre, czmq, and zmq.
    <use project = "zyre" />
    -->

    <!-- 
        The pkg-config based dependencies are added to _CPPFLAGS and _LDADD
    <package_dependency name="zmq" pkg_name="libzmq" for_all="1" />
    -->

    <!-- Header Files 
         name := The name the header file to include without file ending
    <header name = "myproject_prelude" />
    -->

    <!-- 
        Classes, if the class header or source file doesn't exist this will
                 generate a skeletons for them.
                 use private = "1" for internal classes
    <class name = "myclass">Public class description</class>
    <class name = "someother" private = "1">Private class description</class>
    -->

    <!--
        Main programs built by the project
                 use private = "1" for internal tools
    <main name = "progname">Exported public tool</class>
    <main name = "progname" private = "1">Internal tool</class>
    -->

    <!-- 
        Models that we build using GSL. 
        This will generate a 'make code' target to build the models.
    <model name = "sockopts" />
    <model name = "zgossip" />
    <model name = "zgossip_msg" />
    -->

    <!-- Other source files that we need to package
    <extra name = "some_ressource" />
    -->

    <!-- 
        Stuff that needs to be installed:
        
        * Linux -> /usr/local/bin
    -->
    <bin name = "zproject.gsl" />
    <bin name = "zproject_projects.gsl" />
    
    <bin name = "zproject_android.gsl" />
    <bin name = "zproject_autoconf.gsl" />
    <bin name = "zproject_automake.gsl" />
    <bin name = "zproject_ci.gsl" />
    <bin name = "zproject_class.gsl" />
    <bin name = "zproject_cmake.gsl" />
    <bin name = "zproject_docs.gsl" />
    <bin name = "zproject_lib.gsl" />
    <bin name = "zproject_mingw32.gsl" />
    <bin name = "zproject_mkman" />
    <bin name = "zproject_qt_android.gsl" />
    <bin name = "zproject_vs2008.gsl" />
    <bin name = "zproject_vs2010.gsl" />
    <bin name = "zproject_vs2012.gsl" />
    <bin name = "zproject_vs2013.gsl" />

</project>

<A name="toc2-159" title="Installation" />
## Installation

Before you start you'll need to install the code generator GSL (https://github.com/imatix/gsl) on your system. Then execute the generate.sh script to generate the build environment files for zproject.

    ./generate.sh

After that proceed with your favorite build environment. (Currently only autotools!)

<A name="toc3-168" title="autotools" />
### autotools

The following will install the `zproject-*.gsl` files to `/usr/local/bin` where gsl will find them if you use zproject in your project.

    ./autogen.sh
    ./configure
    make
    make install

<A name="toc2-178" title="Generate build environment in your project" />
## Generate build environment in your project

Copy the `project.xml` and `generate.sh` to your project or an empty directory and adjust the values accordingly.

Run `./generate.sh`

<A name="toc2-185" title="Removal" />
## Removal

<A name="toc3-188" title="autotools" />
### autotools

    make uninstall


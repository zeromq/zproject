
<A name="toc1-3" title="zproject - Class Project Generator" />
# zproject - Class Project Generator

<A name="toc2-6" title="Contents" />
## Contents


**<a href="#toc2-11">Overview</a>**
&emsp;<a href="#toc3-18">Scope and Goals</a>

**<a href="#toc2-46">Demo on PLAYTerm</a>**

**<a href="#toc2-51">Installation</a>**
&emsp;<a href="#toc3-54">Requirements</a>
&emsp;<a href="#toc3-66">Getting started</a>

**<a href="#toc2-84">Setup your project environment</a>**

**<a href="#toc2-106">Configuration</a>**

**<a href="#toc2-113">Sample API model</a>**

**<a href="#toc2-154">Ownership and License</a>**

**<a href="#toc2-163">Removal</a>**
&emsp;<a href="#toc3-166">autotools</a>
&emsp;<a href="#toc3-171">Hints to Contributors</a>
&emsp;<a href="#toc3-178">This Document</a>

<A name="toc2-11" title="Overview" />
## Overview

zproject is a community project, like most ZeroMQ projects, built using the C4.1 process, and licensed under MPL v2. It solves the Makefile problem really well. It is unashamedly for C, and more pointedly, for that modern C dialect we call CLASS. CLASS is the Minecraft of C: fun, easy, playful, mind-opening, and social. Read more about it [hintjens#79](http://hintjens.com/blog:79).

zproject grew out of the work that has been done to automatically generate the build environment in CZMQ. It allows to share these automations with other projects like [zyre](https://github.com/zeromq/zyre), [malamute](https://github.com/zeromq/malamute) or [hydra](https://github.com/edgenet/hydra) and at the same time keep everything in sync. 

<A name="toc3-18" title="Scope and Goals" />
### Scope and Goals

zproject has these primary goals:

* generate files for cross-platform build environments.
* generate CLASS ([ZeroMQ RFC/21](http://rfc.zeromq.org/spec:21)) compliant header and source skeletons for new classes.
* generate a public header file for your library so it can be easily included by others. 
* generate stubs for man page documentation which uses the comment based approach from CZMQ.

All you need is a project.xml file in the project's root directory which is your 

    One file to rule them all

The following build environments are currently supported:
 
* android
* autotools 
* cmake 
* mingw32 
* qt-android 
* vs2008 
* vs2010 
* vs2012 
* vs2013 

Thanks to the amazing ZeroMQ community you can do all the heavy lifting in C and than easily generate bindings to Python, Ruby and QML to write a nice GUI on top of it.

<A name="toc2-46" title="Demo on PLAYTerm" />
## Demo on PLAYTerm

There is a short Demo on PLAYTerm that shows how easy it is to get started with zproject: [ZeroMQ - Create new zproject](http://www.playterm.org/r/zeromq---create-new-zproject-1424116766) 

<A name="toc2-51" title="Installation" />
## Installation

<A name="toc3-54" title="Requirements" />
### Requirements

zproject uses the universal code generator called GSL to process its XML inputs and create its outputs. Before you start you'll need to install GSL (https://github.com/imatix/gsl) on your system.

	git clone https://github.com/imatix/gsl.git
	cd gsl
	./autogen.sh
	./configure
	make
	make install

<A name="toc3-66" title="Getting started" />
### Getting started

GSL must be able to find the zproject resources on your system. Therefore you'll need to install them.

The following will install the zproject files to `/usr/local/bin`.

	git clone https://github.com/zeromq/zproject.git
	cd zproject
    ./autogen.sh
    ./configure
    make
    make install

NB: You may need to use the `sudo` command when running `make install` to elevate your privileges, e.g.

	sudo make install

<A name="toc2-84" title="Setup your project environment" />
## Setup your project environment

The easiest way to start is by coping the `project.xml` and `generate.sh` to your project or an empty directory. Licensing your project is important thus you'll need a license file. To get started you can copy `license.xml` from zproject and change the license to whatever you like. Here's an overview that might help you decide to [choose a license](http://choosealicense.com/). The text in the `license.xml` will be placed on every generated header and source file. Thus make sure not to insert the hole license but an appropriate disclaimer.

	mkdir myproject
	cd myproject
	cp ~/zproject/project.xml .
	cp ~/zproject/license.xml .
	cp ~/zproject/generate.sh .

Next, edit `project.xml` to your liking, see [Configuration](#Configuration). Once you're done you can create your project's build environment:

	./generate.sh
	./autogen.sh
	./configure.sh
	make

The compilation will probably fail as the generated skeleton source files are containing empty structs. You'll need to run the `generate.sh` script only when changing the zproject configuration. Otherwise stick to your favorite build environment. To also build the tests (assuming you have added some), use:

	make check

<A name="toc2-106" title="Configuration" />
## Configuration

zproject's `project.xml` contains an extensive description of the available configuration: The following snippet is taken from the `project.xml`:

<!-- 
    The project.xml generates build environments for:

        * android
        * autotool
        * cmake
        * mingw32
        * cygwin
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
        Specify which other projects this depends on.
        These projects must be known by zproject, and the list of
        known projects is maintained in the zproject_known_projects.xml model.
        You need not specify subdependencies if they are implied.
    <use project = "zyre" min_major= "1" min_minor = "1" min_patch = "0" />
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
        Actors, are build using the simple actor framework from czmq. If the 
        actors class header or source file doesn't exist this will generate a
        skeleton for them. The generated test method of the actor will teach
        you how to use them. Also have a look at the czmq docs to learn more
        about actors.
    <actor name = "myactor">Public actor description</actor>
    <actor name = "someactor" private = "1">Private actor description</actor>
    -->
    
    <!--
        Main programs built by the project
                 use private = "1" for internal tools
    <main name = "progname">Exported public tool</main>
    <main name = "progname" private = "1">Internal tool</main>
    <main name = "progname" service = "1">Installed as system service</main>
    -->

    <!-- 
        Models that we build using GSL. 
        This will generate a 'make code' target to build the models.
    <model name = "sockopts" />
    <model name = "zgossip" />
    <model name = "zgossip_msg" />

        If a model should be generated using a specific gsl script,
        this can be set through the script attribute:
    <model name = "hydra_msg" script = "zproto_codec_java.gsl" />

        Additional parameters to the script can be set via nested
        param elements:
    <model name = "hydra_msg" script = "zproto_codec_java.gsl">
        <param name = "root_path" value = "../main" />
    </model>
    -->

    <!-- Other source files that we need to package
    <extra name = "some_ressource" />
    -->

    <!-- 
        Stuff that needs to be installed:

        NOTICE: If you copied this file to get started you want to delete or
                at least comment out those bin tag as they distribute the
                zproject files.
        
        * Linux -> /usr/local/bin
    -->
    <bin name = "zproject.gsl" />
    <bin name = "zproject_projects.gsl" />
    <bin name = "zproject_known_projects.xml" />
    <bin name = "zproject_class_api.gsl" />
    <bin name = "zproject_mkman" />
    
    <bin name = "zproject_actor.gsl" />
    <bin name = "zproject_android.gsl" />
    <bin name = "zproject_autoconf.gsl" />
    <bin name = "zproject_automake.gsl" />
    <bin name = "zproject_bindings_python.gsl" />
    <bin name = "zproject_bindings_qml.gsl" />
    <bin name = "zproject_bindings_ruby.gsl" />
    <bin name = "zproject_ci.gsl" />
    <bin name = "zproject_class.gsl" />
    <bin name = "zproject_cmake.gsl" />
    <bin name = "zproject_docs.gsl" />
    <bin name = "zproject_git.gsl" />
    <bin name = "zproject_lib.gsl" />
    <bin name = "zproject_mingw32.gsl" />
    <bin name = "zproject_cygwin.gsl" />
    <bin name = "zproject_qt_android.gsl" />
    <bin name = "zproject_tools.gsl" />
    <bin name = "zproject_vs2008.gsl" />
    <bin name = "zproject_vs2010.gsl" />
    <bin name = "zproject_vs2012.gsl" />
    <bin name = "zproject_vs2013.gsl" />
</project>

<A name="toc2-113" title="Sample API model" />
## Sample API model

The zproject scripts can also optionally generate the `@interface` in your class headers from an API model, in addition to a host of language bindings.  To opt-in to this behavior, just make a model to the `api` directory of your project.  For example, if your `project.xml` contains `<class name = "myclass"/>`, you could create the following `api/myclass.xml` file:

<!--
    This model defines a public API for binding. 
-->
<class name = "myclass" >
    My Feature-Rich Class

    <include filename = "../license.xml" />

    <constant name = "default port" value = "8080">registered with IANA</constant>

    <!-- Constructor is optional; default one has no arguments -->
    <constructor>
        Create a new myclass with the given name.
        <argument name = "name" type = "string" />
    </constructor>

    <!-- Destructor is optional; default one follows standard style -->
    <destructor />

    <!-- This models a method with no return value -->
    <method name = "sleep">
        Put the myclass to sleep for the given number of milliseconds.
        No messages will be processed by the actor during this time.
        <argument name = "duration" type = "integer" />
    </method>

    <!-- This models an accessor method -->
    <method name = "has feature">
        Return true if the myclass has the given feature.
        <argument name = "feature" type = "string" />
        <return type = "boolean" />
    </method>

    <!-- Callback typedefs can be declared like methods -->
    <callback_type name = "handler_fn">
        <argument name = "self" type = "myclass" />
        <argument name = "action" type = "string" />
        <return type = "boolean" />
    </callback_type>

    <!-- Callback types can be used as method arguments -->
    <method name = "add handler">
        Store the given callback function for later
        <argument name = "handler" type = "myclass_handler_fn" callback = "1" />
    </method>

    <!-- If singleton = "1", no class struct pointer is required. -->
    <method name = "test" singleton = "1">
        Self test of this class
        <argument name = "verbose" type = "boolean" />
    </method>

    <!-- These are the types we support
         Not all of these are supported in all language bindings;
         see each language binding's file for supported types in that
         language, and add more types as needed where appropriate.
         -->
    <method name = "tutorial">
        <argument name = "void pointer" type = "anything" />
        <argument name = "standard int" type = "integer" />
        <argument name = "standard float" type = "real" />
        <argument name = "standard bool" type = "boolean" />
        <argument name = "char pointer" type = "string" />
        <argument name = "custom pointer" type = "myclass_t" />
        <return type = "nothing">void method</return>
    </method>
</class>

This would cause the following `@interface` to be generated inside of `include/myclass.h`.  Note that if `include/myclass.h` has other handwritten content outside of the `@interface` this content will be retained.

    //  @warning THE FOLLOWING @INTERFACE BLOCK IS AUTO-GENERATED BY ZPROJECT!
    //  @warning Please edit the model at "api/myclass.xml" to make changes.
    //  @interface
    //  Create a new myclass with the given name.
    MYPROJECT_EXPORT myclass_t *
        myclass_new (const char *name);

    //  Destroy the myclass.
    MYPROJECT_EXPORT void
        myclass_destroy (myclass_t **self_p);

    //  Return true if the myclass has the given feature.
    MYPROJECT_EXPORT bool
        myclass_has_feature (myclass_t *self, const char *feature);

    //  Put the myclass to sleep for the given number of milliseconds.
    //  No messages will be processed by the actor during this time.  
    MYPROJECT_EXPORT void
        myclass_sleep (myclass_t *self, int duration);

    //  Self test of this class
    MYPROJECT_EXPORT void
        myclass_test (bool verbose);
    //  @end

Language bindings will also be generated in the following languages:

* Ruby (experimental)
* QML (experimental)

The language bindings are minimal, meant to be wrapped in a handwritten idiomatic layer later.

<A name="toc2-154" title="Ownership and License" />
## Ownership and License

The contributors are listed in AUTHORS. This project uses the MPL v2 license, see LICENSE.

zproject uses the [C4.1 (Collective Code Construction Contract)](http://rfc.zeromq.org/spec:22) process for contributions.

To report an issue, use the [zproject issue tracker](https://github.com/zeromq/zproject/issues) at github.com.

<A name="toc2-163" title="Removal" />
## Removal

<A name="toc3-166" title="autotools" />
### autotools

    make uninstall

<A name="toc3-171" title="Hints to Contributors" />
### Hints to Contributors

Before you commit code please make sure that the project model hides all details of backend scripts.

For example don't make a user enter a header file because autoconf needs it to do AC_CHECK_LIB.

<A name="toc3-178" title="This Document" />
### This Document

This document is originally at README.txt and is built using [gitdown](http://github.com/imatix/gitdown).

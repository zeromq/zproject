zproject - a project skeleton generator
=======================================

zproject does several things:

* generate files for cross-platform build environments
* generate a main header for your library (e.g. czmq.h, zyre.h)
* ~~generate a prelude header for cross-platform settings (e.g. czmq_prelude.h)~~
* generate a header for private classes (e.g. src/zyre_classes.h)
* generate header and source skeletons for new class

All you need is a project.xml file which is your 

```One file to rule them all```

The following build environments are currently supported:
 
* android (not tested)
* autotools (tested)                                                                                   
* cmake (not tested)                                                                                
* mingw32 (not tested)                                                                                    
* vs2008 (not tested)                                                                                     
* vs2010 (not tested)
* vs2012 (not tested)
* vs2013 (not tested)
 
All classes in the project.xml are automatically added to all build environments. Further as you
add new classes to your project you can generate skeleton header and source files according to http://rfc.zeromq.org/spec:21.

# project.xml tags

## class
Classes can be public, in which case header files are expected or generated into `include` directory.
```
<class name = "myclass" >My class's description</class>
```

And classes can be private, in which case header files are expected or generated into `src` directory.

```
<class name = "myclass" priavte = "1" >My private class's description</class>
```
Public classes will be included in the main header file which equals your projects name. Private classes will be included into a different header file in the `src` directory which in named "project name + _classes.h".

## header
Headers for classes are automatically added, there's no need to add them by header tag. If you've other headers besides the one for your classes, you can add them by specifying the name and optionally a placement option. The header file will be assumed to be in the `include` directory and will the included into the main header files. By default it is put on the top after the dependencies. If you like to put it below the typedef's of the classes structs in the main header file you can specify `placement="post"`.
```
 <header name = "myproject_magic" placement ="pre|post" />
```

##  dependency
Dependencies to other libraries need three attributes. The name of the library (without lib prefix), their header file to be included and a test method to check if the library is installed. (Currently only dynamic linked libraries are supported). Below is an example for zeromq/libzmq:

```
<dependency name="zmq" header="zmq.h" test="zmq_init" />
```

## more is comming ...

Have a look at the project.xml which has further information.

# Install

Before you start you'll need to install the code generator GSL (https://github.com/imatix/gsl) on your system. Then execute the generate.sh script to generate the build environment files for zproject.

```
./generate.sh
```
After that proceed with your favorite build environment. (Currently only autotools!)

## autotools
The following will install the `build-*.gsl` files to `/usr/local/bin` where gsl will find them if you use zproject in your project.
```
./autogen.sh
./configure
make
make install
```

# Generate build environment in your project

Copy the `project.xml` and `generate.sh` to your project or an empty directory and adjust the values accordingly.

Run `./generate.sh`

# Uninstall

## autotools

```
make uninstall
```

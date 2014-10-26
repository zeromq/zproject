zproject - a project skeleton generator
=======================================

zproject does several things:

* generate files for cross-platform build environments
* generate header and sources files for new class

All you is a project.xml file. This is your 

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
 
Classes are automatically added to all build environments. Further as you
add new classes to your project you can generate skeleton header and source 
files according to http://rfc.zeromq.org/spec:21.

# Install

```
./generate.sh
```

## autotools

```
./autogen.sh
./configure
make
make install
```

# Generate 

Copy the `project.xml` and `generate.sh` to your project or an empty directory and adjust the values accordingly.

Run `./generate.sh`

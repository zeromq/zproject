
<A name="toc1-3" title="zproject - Class Project Generator" />
# zproject - Class Project Generator

<A name="toc2-6" title="Contents" />
## Contents


**<a href="#toc2-11">Overview</a>**
&emsp;<a href="#toc3-18">Scope and Goals</a>

**<a href="#toc2-50">Demo on PLAYTerm</a>**

**<a href="#toc2-55">Installation</a>**
&emsp;<a href="#toc3-58">Requirements</a>
&emsp;<a href="#toc3-70">Getting started</a>

**<a href="#toc2-94">Setup your project environment</a>**

**<a href="#toc2-131">Configuration</a>**

**<a href="#toc2-313">Sample API model</a>**
&emsp;<a href="#toc3-526">Supported API Model Attributes</a>
&emsp;<a href="#toc3-542">API Types</a>
&emsp;<a href="#toc3-581">Tips</a>
&emsp;<a href="#toc3-598">Generate API model from C header files</a>
&emsp;<a href="#toc4-620">Known caveats</a>

**<a href="#toc2-625">Language Binding Notes</a>**
&emsp;<a href="#toc3-628">Java Language Binding</a>

**<a href="#toc2-636">Draft API Support</a>**

**<a href="#toc2-668">Targets</a>**

**<a href="#toc2-694">Removal</a>**
&emsp;<a href="#toc3-697">autotools</a>

**<a href="#toc2-704">Notes for Writing Language Targets</a>**
&emsp;<a href="#toc3-724">Schema/Architecture Overview</a>
&emsp;<a href="#toc3-743">Informal Summary</a>
&emsp;<a href="#toc3-748">Semantic Attributes</a>
&emsp;<a href="#toc3-783">Target Scopes</a>
&emsp;<a href="#toc3-788">Target Options</a>

**<a href="#toc2-816">Ownership and License</a>**
&emsp;<a href="#toc3-825">Hints to Contributors</a>
&emsp;<a href="#toc3-834">This Document</a>

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

At least the following build environments are currently supported:

* Autotools
* CMake
* Mingw32
* Android
* Visual Studio

Thanks to the ZeroMQ community, you can do all the heavy lifting in C and then easily generate bindings in the following languages:

* Java (JNI)
* Python
* QML
* Qt
* Ruby

The language bindings are minimal, meant to be wrapped in a handwritten idiomatic layer later.

<A name="toc2-50" title="Demo on PLAYTerm" />
## Demo on PLAYTerm

There is a short Demo on PLAYTerm that shows how easy it is to get started with zproject: [ZeroMQ - Create new zproject](http://www.playterm.org/r/zeromq---create-new-zproject-1424116766)

<A name="toc2-55" title="Installation" />
## Installation

<A name="toc3-58" title="Requirements" />
### Requirements

zproject uses the universal code generator called GSL to process its XML inputs and create its outputs. Before you start you'll need to install GSL (https://github.com/imatix/gsl) on your system.

```sh
git clone https://github.com/imatix/gsl.git
cd gsl/src
make
make install
```

<A name="toc3-70" title="Getting started" />
### Getting started

GSL must be able to find the zproject resources on your system. Therefore you'll need to install them.

The following will install the zproject files to `/usr/local/bin`.

```sh
git clone https://github.com/zeromq/zproject.git
cd zproject
autogen.sh
configure
make
make install
```

NB: You may need to use the `sudo` command when running `make install` to elevate your privileges, e.g.

```sh
sudo make install
```

NB: If you don't have superuser rights on a system you'll have to make sure zproject's gsl scripts can be found on your PATH.

<A name="toc2-94" title="Setup your project environment" />
## Setup your project environment

The easiest way to start is to create a minimal project.xml.

```xml
<project script = "zproject.gsl">
    <use project = "czmq" />
    <main name = "hello" private = "1" />
</project>
```

Once you're done you can create your project's build environment and start compiling:

```sh
gsl project.xml
autogen.sh
configure.sh
make
```

NB: To get a more comprehensive example copy zproject's project.xml. It contains all possible configurations and according documentation.

Licensing your project is important thus you'll need a license file. Here's an overview that might help you decide to [choose a license](http://choosealicense.com/). zproject allows you to add an appropriate disclaimer of your license as a xml file, e.g. license.xml:

```xml
<license>
    Your license disclaimer goes here!
</license>
```

This disclaimer can be included in your project.xml and is used whenever zproject is generating new files e.g. CLASS skeletons or bindings.

```xml
<include filename = "license.xml" />
```

<A name="toc2-131" title="Configuration" />
## Configuration

zproject's `project.xml` contains an extensive description of the available configuration: The following snippet is taken from the `project.xml`:

```xml
<!--
    The project.xml generates build environments for:

        autotools           GNU build system (default)
        cmake               CMake build system (default)

        android             Native shared library for Android
        cygwin              Cygwin build system
        debian              packaging for Debian
        docker              packaging for Docker
        java                Java JNI binding
        java-msvc           MSVC builds for Java JNI binding
        mingw32             Mingw32 build system
        nuget               Packaging for NuGet
        python              Python binding
        qml                 QML binding
        qt                  Qt binding
        redhat              Packaging for RedHat
        ruby                Ruby binding
        travis              Travis CI scripts
        vs2008              Microsoft Visual Studio 2008
        vs2010              Microsoft Visual Studio 2010
        vs2012              Microsoft Visual Studio 2012
        vs2013              Microsoft Visual Studio 2013
        vs2015              Microsoft Visual Studio 2015

    Classes are automatically added to all build environments. Further as you
    add new classes to your project you can generate skeleton header and source
    files according to http://rfc.zeromq.org/spec:21.

    script := The gsl script to generate all the stuff !!! DO NOT CHANGE !!!
    name := The name of your project (optional)
    description := A short description for your project (optional)
    email := The email address where to reach you (optional)
    repository := git repository holding project (optional)
-->
<project script = "zproject.gsl" name = "myproject">

    <!--
        Includes are processed first, so XML in included files will be
        part of the XML tree
    -->
    <include filename = "license.xml" />

    <!--
        Current version of your project.
        This will be used to package your distribution
    -->
    <version major = "1" minor = "1" patch = "0" />

    <!--
        Specify which other projects this depends on.
        These projects must be known by zproject, and the list of
        known projects is maintained in the zproject_known_projects.xml model.
        You need not specify subdependencies if they are implied.
        Dependencies that support the autotools build system are automatically
        build by travis ci if you supply a git repository or a tarball URI.
    <use project = "zyre" min_major= "1" min_minor = "1" min_patch = "0" />
    <use project = "uuid" optional= "1" implied = "1" />
    <use project = "myfirstlib" repository = "http://myfirstlib.org/myfirstlib.git" />
    <use project = "mysecondlib" tarball = "http://mysecondlib.org/mysecondlib-1.2.3.tar.gz" />
    -->

    <!-- Header Files
         name := The name the header file to include without file ending
    <header name = "myproject_prelude" />
    -->

    <!--
        Classes, if the class header or source file doesn't exist, this will
        generate a skeletons for them.
        use private = "1" for internal classes
    <class name = "myclass">Public class description</class>
    <class name = "someother" private = "1">Private class description</class>
    -->

    <!--
        Actors, are built using the simple actor framework from czmq. If the
        actors class header or source file doesn't exist, this will generate a
        skeleton for them. The generated test method of the actor will teach
        you how to use them. Also have a look at the CZMQ docs to learn more
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
        Benchmark programs built by the project
    <bench name = "benchname">Benchmark for class/function...</main>
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
    <extra name = "some_resource" />
    -->
    <!-- Specify targets to build; autotools and cmake are
         built in all cases.
    <target name = "cmake" />
    <target name = "autotools" />
    -->
    <!-- Targets may be customizable with their own options -->
    <target name = "cmake">
        <option name = "single setting" value = "value" />
        <option name = "list setting">
            <item name = "item name" value = "item value" />
        </option>
    </target>

    <!-- In order loaded by zproject.gsl -->
    <bin name = "zproject.gsl" />
    <bin name = "zproject_projects.gsl" />
    <bin name = "zproject_class_api.gsl" />

    <!-- Mainline generation code -->
    <bin name = "zproject_skeletons.gsl" />
    <bin name = "zproject_bench.gsl" />
    <bin name = "zproject_class.gsl" />
    <bin name = "zproject_git.gsl" />
    <bin name = "zproject_valgrind.gsl" />

    <!-- Targets -->
    <bin name = "zproject_android.gsl" />
    <bin name = "zproject_autotools.gsl" />
    <bin name = "zproject_cmake.gsl" />
    <bin name = "zproject_cygwin.gsl" />
    <bin name = "zproject_debian.gsl" />
    <bin name = "zproject_docker.gsl" />
    <bin name = "zproject_gyp.gsl" />
    <bin name = "zproject_java.gsl" />
    <bin name = "zproject_java_lib.gsl" />
    <bin name = "zproject_java_msvc.gsl" />
    <bin name = "zproject_mingw32.gsl" />
    <bin name = "zproject_nodejs.gsl" />
    <bin name = "zproject_nuget.gsl" />
    <bin name = "zproject_python.gsl" />
    <bin name = "zproject_python_cffi.gsl" />
    <bin name = "zproject_qml.gsl" />
    <bin name = "zproject_qt.gsl" />
    <bin name = "zproject_redhat.gsl" />
    <bin name = "zproject_ruby.gsl" />
    <bin name = "zproject_travis.gsl" />
    <bin name = "zproject_vs2008.gsl" />
    <bin name = "zproject_vs20xx.gsl" />
    <bin name = "zproject_vs20xx_props.gsl" />

    <bin name = "zproject_known_projects.xml" />
    <bin name = "mkapi.py" />
    <bin name = "fake_cpp" />
</project>
```

<A name="toc2-313" title="Sample API model" />
## Sample API model

The zproject scripts can also optionally generate the `@interface` in your class headers from an API model, in addition to a host of language bindings.  To opt-in to this behavior, just make a model to the `api` directory of your project.  For example, if your `project.xml` contains `<class name = "myclass"/>`, you could create the following `api/myclass.api` file:

```xml
<!--
    This model defines a public API for binding.

    It shows a language binding developer what to expect from the API XML
    files.
-->
<class name = "myclass" >
    My Feature-Rich Class

    <include filename = "license.xml" />

    <constant name = "default port" value = "8080">registered with IANA</constant>

    <constant name = "normal" value = "1">
    <constant name = "fast"   value = "2">
    <constant name = "safe"   value = "3">

    <!-- Constructor is optional; default one has no arguments -->
    <constructor>
        Create a new myclass with the given name.
        <argument name = "name" type = "string" />
    </constructor>

    <!-- Destructor is optional; default one follows standard style -->
    <destructor>
        Destructors implicitely get a new argument prepended, which:

        * is called `self_p`
        * is of this class' type
        * is passed by reference
        * is marked as the self pointer for the destructor (`destructor_self = "1"`)
    </destructor>

    <!-- This models an CZMQ actor. By default the actor method equals the
         class name.
    -->
    <actor>
        To work with my_actor, use the CZMQ zactor API:

        Create new my_actor instance.

            zactor_t *actor = zactor_new (my_actor, NULL);

        Destroy my_actor instance

            zactor_destroy (&amp;actor);

        Enable verbose logging of commands and activity:

            zstr_send (actor, "VERBOSE");
    </actor>

    <!-- This models a method with no return value -->
    <method name = "sleep">
        Put the myclass to sleep for the given number of milliseconds.
        No messages will be processed by it during this time.
        <argument name = "duration" type = "integer" />
    </method>

    <!-- This models an accessor method -->
    <method name = "has feature">
        Return true if the myclass has the given feature.
        <argument name = "feature" type = "string" />
        <return type = "boolean" />
    </method>

    <method name = "send strings">
        This does something with a series of strings (until NULL). The strings
        won't be touched.

        Because the next method has the same name with a prepended "v", it's
        recognized as this method's `va_list` sibling (in GSL:
        `method.has_va_list_sibling = "1"`). This information might be used by
        the various language bindings.
        <argument name = "string" type = "string" variadic = "1" />
        <return type = "boolean" />
    </method>
    <method name = "vsend strings">
        This does something with a series of strings (until NULL). The strings
        won't be touched (they're declared immutable by default).
        <argument name = "string" type = "string" variadic = "1" />
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
        <argument name = "handler" type = "my_class_handler_fn" callback = "1" />
    </method>

    <!-- If singleton = "1", no class struct pointer is required. -->
    <method name = "test" singleton = "1">
        Self test of this class
        <argument name = "verbose" type = "boolean" />
    </method>

    <method name = "new thing" singleton = "1" >
	Creates a new myclass. The caller is responsible for destroying it when
	finished with it.
        <return type = "myclass" fresh = "1" />
    </method>

    <method name = "free" singleton = "1">
        Frees a provided string, and nullify the parent pointer. Setting
        `mutable = "1"` is not needed here, because transfering ownership from
        the caller to the function using `by_reference = "1"` implies that it's
        mutable.
        <argument name = "string pointer" type = "string" by_reference = "1" />
    </method>

    <method name = "rotate" singleton = "1">
        Rotates the characters in `data` in-place. This means that all
        characters are shifted to the left by one, removing the left-most
        character and appending it to the end.
        <argument name = "data" type = "string" mutable = "1" />
    </method>

    <!-- These are the types we support
         Not all of these are supported in all language bindings;
         see each language binding's file for supported types in that
         language, and add more types as needed where appropriate.

         Also, see zproject_class_api.gsl to see how they're handled exactly.
         -->
    <method name = "tutorial">
        <argument name = "void pointer" type = "anything" />
        <argument name = "standard int" type = "integer" />
        <argument name = "standard float" type = "real" />
        <argument name = "standard bool" type = "boolean" />
        <argument name = "fixed size unsigned integer" type = "number" size = "4">
            Supported sizes are 1, 2, 4, and 8.
        </argument>
        <argument name = "a byte" type = "byte" />
        <argument name = "conversion mode" type = "integer" />
        <argument name = "char pointer to C string" type = "string" />
        <argument name = "byte pointer to buffer" type = "buffer" />
        <argument name = "buffer size" type = "size" />
        <argument name = "file handle" type = "FILE" />
        <argument name = "file size" type = "file_size" />
        <argument name = "time" type = "time" />
        <argument name = "format" type = "format">
            This makes the function is variadic (will cause a new argument to be
            added to represent the variadic arguments).
        </argument>
        <argument name = "variadic list argument" type = "va_list" />
        <argument name = "custom pointer" type = "my custom class">
            Any other type is valid, as long as there is a corresponding C
            type, in this case `my_custom_class_t`.
        </argument>
        <return type = "nothing">void method</return>
    </method>

    <method name = "set foo" polymorphic = "1">
      Set attribute foo to a new value. Note that this method takes a
      polymorphic reference (`void *`) as its first argument, which could point
      to structs of different types.

      This also means that high-level bindings might give you the choice to
      call this method directly on an instance, or with an explicit receiver.
      <argument name = "new value" type="integer" />
    </method>

    <method name = "set bar">
        This method takes an argument type of the (descriptive) type `foo`, but
        resolving it to a corresponding C type will be skipped because it's
        overridden to `foobarbaz_t` by the `c_type` attribute.
        <argument name = "new foo" type="foo" c_type="foobarbaz_t" />
    </method>
</class>
```

This would cause the following `@interface` to be generated inside of `include/myclass.h`.  Note that if `include/myclass.h` has other handwritten content outside of the `@interface` this content will be retained.

```c
//  @warning THE FOLLOWING @INTERFACE BLOCK IS AUTO-GENERATED BY ZPROJECT!
//  @warning Please edit the model at "api/myclass.api" to make changes.
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
```

<A name="toc3-526" title="Supported API Model Attributes" />
### Supported API Model Attributes

The following attributes are supported for methods:

- `name` - the name of the method (mandatory).
- `singleton = "1"` - the method is not invoked within the context of a specific instance of an object. Use this if your method does not need to be passed a `self` pointer as the first argument as normal. Implicit for all `constructor`s and `destructor`s and for the implicit `test` method.

The following attributes are supported for arguments and return values:

- `type` - the conceptual type or class name of the argument or return value (default: `"nothing"`, which translates to `void` in C).
- `mutable = "1"` - the argument or the return value can be modified. All string, format, and buffer arguments are immutable by default.
- `by_reference = "1"` - ownership of the argument (and responsibility for freeing it) is transferred from the caller to the function - in practice, the implementation code should also nullify the caller's reference, though this is not enforced by the API model. If a string or buffer is passed by reference, it is also mutable by default.
- `fresh = "1"` - the return value is freshly allocated, and the caller receives ownership of the object and the responsibility for destroying it. Implies mutable = "1".
- `variadic = "1"` - used for representing variadic arguments.

<A name="toc3-542" title="API Types" />
### API Types

This is an incomplete list of API types:

* "nothing" -- for return only, means "void" in C.

* "anything" -- means "void *" in C.

* "size" -- long size (64 bits), "size_t" in C.

* "time" -- long time (64 bits), "time_t" in C.

* "file_size" -- long file size (64 bits).

* "boolean" -- Boolean.

* "byte" -- single octet.

* "char" -- single character (possibly multibyte, do we care?)

* "integer" -- 32-bit signed integer.

* "number" -- unsigned number, with 'size = "1|2|4|8"'.

* "real" -- single-precision floating point. [TODO: single? why not double?]

* "buffer" -- byte array. To return a byte array, you should specify 'size' attribute that defines size. This can be a constant, 'size = "ZUUID_LEN"', or a dot followed by method name in the same class, e.g. 'size = ".size"'.

* "string" -- character array.

* "format" -- printf format, followed by zero or more arguments.

* "FILE", "va_list", "zmq_pollitem", "socket" -- literally that, in C. (Not sure if it is wise to use raw C types.)

* callbacks - tbd.

* Names of classes, e.g. zmsg.

<A name="toc3-581" title="Tips" />
### Tips

At any time, you can examine a resolved model as an XML string with all of its children and attributes using the appropriate GSL functions:

```gsl
 # if the `method` variable is a <method/> entity:
echo method.string()  # will print the model as an XML string.
method.save(filename) # will save the model as an XML string to the given file.
```

You can save a snapshot of the entire resolved project model using this syntax:

```
gsl -save:1 project.xml
```

<A name="toc3-598" title="Generate API model from C header files" />
### Generate API model from C header files

Writing API model for bigger project with a lot of classes can be tedious job. There mkapi.py, which automates most of the task.

In order to use it, you must install zproject itself and then pycparser. For most of real world code, you must have fake_libc_includes available too.
```sh
virtualenv/venv mkapi
source mkapi/bin/activate
pip install pycparser
git clone https://github.com/eliben/pycparser.git
```

Then from root directory of your project (for example czmq), type following
```sh
mkapi.py -I /path/to/your/pycparser/utils/fake_libc_include include/czmq.h
```

Note you *must* use top-level include as pycparser fails if it does not know any definition.

The tool might expect `-DWITH_DRAFTS` parameter if the class is not marked as a stable.

<A name="toc4-620" title="Known caveats" />
#### Known caveats

The tool can't distinguish methods which allocates new object. It does print a comment about adding fresh = "1" attribute to each method, which return non const pointer. However the final assigment must be done manually.

<A name="toc2-625" title="Language Binding Notes" />
## Language Binding Notes

<A name="toc3-628" title="Java Language Binding" />
### Java Language Binding

* Skips methods that it cannot handle properly.

* To build, you need gradle (or equivalent). Run 'gradle build jar' in the bindings/jni directory.
* To install, run 'gradle install'. This puts the files into $HOME/.m2/repository.

<A name="toc2-636" title="Draft API Support" />
## Draft API Support

zproject lets you mark classes and methods as 'draft' so that they are not installed by default in stable builds. This lets you deliver draft APIs to your users, and change them later.

By default all classes and methods are draft, unless you specify otherwise. To mark the state of a class or method, specify in the project.xml:

```
<class name = "classname" state = "stable" />
```

Or in the class API XML file:

```
<class name = "classname" state = "stable">
    ...
    <method name = "methodname" state = "stable">
        ...
    </method>
</class>
```

The method will inherit the class state unless it has its own 'state' attribute.

The allowed states are:

* draft - the class or method is not built/installed in stable releases.
* stable - the class or method is always built and installed. A method may not be changed once marked as stable.
* legacy - the class or method is always built and installed. It may carry a warning that support can be withdrawn at any time.

Using autotools or CMake, you can specify --with-drafts to enable draft APIs, and --without-drafts to disable them. By default, drafts are built and installed when you work in a git repository (if the directory ".git" is present), and otherwise they are not. That means, if you build from a tarball, drafts are disabled by default.

<A name="toc2-668" title="Targets" />
## Targets

Each target produces scripts and code for a specific build system, platform, or language binding.

To see a list of available targets:

    gsl -target:? project.xml

To build a specific target:

    gsl -target:android project.xml

To run zproject without building any targets:

    gsl -target:- project.xml

To request specific targets in your project.xml file (autotools and cmake are automatic):

    <target name = "android" />
    <target name = "java" />

To request all targets in your project.xml file:

    <target name = "*" />

<A name="toc2-694" title="Removal" />
## Removal

<A name="toc3-697" title="autotools" />
### autotools

```sh
make uninstall
```

<A name="toc2-704" title="Notes for Writing Language Targets" />
## Notes for Writing Language Targets

This is the general form of a target:

```
register_target ("somename", "Decription of target")

function target_somename

\.macro generate_something
    ...
\.endmacro

    project.topdir = "someplace/somename"
    directory.create (project.topdir)
    generate_something ()
endfunction
```

<A name="toc3-724" title="Schema/Architecture Overview" />
### Schema/Architecture Overview

* All `class`es SHALL be in the project model (`project.xml`).
* Each `class` MAY have a corresponding API model (`api/{class name}.api`).
* A binding generator SHOULD consider only `class`es with an API model (`where defined (class.api)`).
* Each API model SHALL consist of both explicit information (written in the XML file) and implicit information (inferred by the [`zproject_class_api`](zproject_class_api.gsl) script). Both kinds of information will already be resolved (and indistinguishable) when each language binding generator is invoked.
* Each API model SHALL have exactly one `class` entity at the top level.
* Each `class` SHALL have a `name` attribute.
* Each `class` MAY have one or more `method` entities.
* Each `class` MAY have one or more `constructor` entities.
* Each `class` MAY have one or more `destructor` entities.
* Each `method`, `constructor`, and `destructor` MAY have one or more `argument` entities.
* Each `method`, `constructor`, and `destructor` SHALL at least one `return` entity, and if more than one `return` entity exist, only the first SHOULD be considered. The `return` entity MAY be ignored if it has `type = "nothing"` (the default when no `type` is given).
* Each entity SHALL have its semantic attributes fully resolved before reaching the language binding generators.
* Each language binding generator SHALL NOT modify values of semantic attributes of entities.
* Each language binding generator MAY assign values to language-specific implementation attributes of entities.
* Each language binding generator SHOULD use a unique prefix for names of language-specific implementation attributes of entities.

<A name="toc3-743" title="Informal Summary" />
### Informal Summary

A `class` is always the top-level entity in an API model, and it will be merged with the corresponding `class` entity defined in the project model. A class contains `method`s, `constructor`s, and `destructor`s (collectively, "method"s), and methods contain `argument`s and `return`s (collectively, "container"s). Each entity will contain both *semantic attributes* and *language-specific implementation attributes*.

<A name="toc3-748" title="Semantic Attributes" />
### Semantic Attributes

Semantic attributes describe something intrinsic about the container.

For example, arguments may be described as passed `by_reference` to indicate that ownership is transferred from the caller. Similarly, return values may be described as `fresh` to indicate that ownership is transferred to the caller, which must destroy the object when it is finished with it. It's important to remember that these attributes are primarily meant to be an abstraction that describes conceptual information, leaving the details of how code generators interpret (or ignore) each attribute up to the authors.

Semantic attributes may be implicit (not given a value in the written model). In this case, it is up to the [`zproject_class_api`](zproject_class_api.gsl) script to fully resolve default values for all attributes. Downstream code generators should *never* resolve or alter semantic attributes, as this could change the behavior of any code generator that is run after the errant code generator.

These are the semantic attributes for each kind of entity that will be resolved before language bindings generators are invoked:

```gsl
class.name        # string (as given in the API model)
class.description # string (comment in the API model, or empty string)
```
```gsl
method.name           # string (as given in the API model, or a default value)
method.description    # string (comment in the API model, or a default value)
method.singleton      # 0/1 (default: 0, but 1 for constructors/destructors)
method.is_constructor # 0/1 (default: 0, but 1 for constructors)
method.is_destructor  # 0/1 (default: 0, but 1 for destructors)
method.has_va_list_sibling # 0/1 (default: 0)
```
```gsl
container.name         # string (as given in the API model, or "_")
container.type         # string (as given, or "nothing")
container.mutable      # 0/1 (default: 0)
container.by_reference # 0/1 (default: 0)
container.callback     # 0/1 (default: 0)
container.fresh        # 0/1 (default: 0)
container.variadic     # 0/1 (default: 0)
container.va_start     # string - that holds the argment name for va_start ()
container.optional     # 0/1 (default: 0), up to binding generator to use
```

<A name="toc3-783" title="Target Scopes" />
### Target Scopes

Each target works in its own copy of 'project'. It can therefore modify and extend 'project' as wanted, without affecting other targets.

<A name="toc3-788" title="Target Options" />
### Target Options

A target can accept options via project.xml like this:

```
<project
    name = "..."
    >
    ...
    <target name = "*" />
    <target name = "nuget">
        <option name = "id" value = "czmq_vc120" />
        <option name = "dependency">
            <item name = "libzmq_vc120" value = "4.2.0.0" />
        </option>
    </target>
</project>
```

This generates all targets (`name = "*"`) and then configures the `nuget` target with options. Zproject aare provided to the target handler as:

```
project.nuget_id = "czmq_vc120"
project.nuget_dependency.name = "libzmq_vc120"
project.nuget_dependency.value = "4.2.0.0"
```

<A name="toc2-816" title="Ownership and License" />
## Ownership and License

The contributors are listed in AUTHORS. This project uses the MPL v2 license, see LICENSE.

zproject uses the [C4.1 (Collective Code Construction Contract)](http://rfc.zeromq.org/spec:22) process for contributions.

To report an issue, use the [zproject issue tracker](https://github.com/zeromq/zproject/issues) at github.com.

<A name="toc3-825" title="Hints to Contributors" />
### Hints to Contributors

Make sure that the project model hides all details of backend scripts. For example don't make a user enter a header file because autoconf needs it.

Do read your code after you write it and ask, "Can I make this simpler?" We do use a nice minimalist and yet readable style. Learn it, adopt it, use it.

Before opening a pull request read our [contribution guidelines](https://github.com/zeromq/zproject/blob/master/CONTRIBUTING.md). Thanks!

<A name="toc3-834" title="This Document" />
### This Document

This document is originally at README.txt and is built using [gitdown](http://github.com/imatix/gitdown).

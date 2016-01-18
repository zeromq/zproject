
<A name="toc1-3" title="zproject - Class Project Generator" />
# zproject - Class Project Generator

<A name="toc2-6" title="Contents" />
## Contents


**<a href="#toc2-11">Overview</a>**
&emsp;<a href="#toc3-18">Scope and Goals</a>

**<a href="#toc2-54">Demo on PLAYTerm</a>**

**<a href="#toc2-59">Installation</a>**
&emsp;<a href="#toc3-62">Requirements</a>
&emsp;<a href="#toc3-74">Getting started</a>

**<a href="#toc2-98">Setup your project environment</a>**

**<a href="#toc2-135">Configuration</a>**

**<a href="#toc2-294">Sample API model</a>**
&emsp;<a href="#toc3-516">Supported API Model Attributes</a>
&emsp;<a href="#toc3-532">API Types</a>
&emsp;<a href="#toc3-573">Tips</a>
&emsp;<a href="#toc3-590">Generate API model from C header files</a>
&emsp;<a href="#toc4-610">Known caveats</a>

**<a href="#toc2-615">Language Binding Notes</a>**
&emsp;<a href="#toc3-618">JNI Language Binding</a>

**<a href="#toc2-626">Draft API Support</a>**

**<a href="#toc2-658">Removal</a>**
&emsp;<a href="#toc3-661">autotools</a>

**<a href="#toc2-668">Notes for Writing Language Bindings</a>**
&emsp;<a href="#toc3-671">Schema/Architecture Overview</a>
&emsp;<a href="#toc3-690">Informal Summary</a>
&emsp;<a href="#toc3-695">Semantic Attributes</a>
&emsp;<a href="#toc3-732">Language-Specific Implementation Attributes</a>

**<a href="#toc2-743">Ownership and License</a>**
&emsp;<a href="#toc3-752">Hints to Contributors</a>
&emsp;<a href="#toc3-761">This Document</a>

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

* autotools
* cmake
* mingw32
* Android
* vs2008
* vs2010
* vs2012
* vs2013
* vs2015

Thanks to the amazing ZeroMQ community, you can do all the heavy lifting in C and then easily generate bindings in the following languages:

* Java (JNI)
* Python
* QML
* Qt
* Ruby

The language bindings are minimal, meant to be wrapped in a handwritten idiomatic layer later.

<A name="toc2-54" title="Demo on PLAYTerm" />
## Demo on PLAYTerm

There is a short Demo on PLAYTerm that shows how easy it is to get started with zproject: [ZeroMQ - Create new zproject](http://www.playterm.org/r/zeromq---create-new-zproject-1424116766)

<A name="toc2-59" title="Installation" />
## Installation

<A name="toc3-62" title="Requirements" />
### Requirements

zproject uses the universal code generator called GSL to process its XML inputs and create its outputs. Before you start you'll need to install GSL (https://github.com/imatix/gsl) on your system.

```sh
git clone https://github.com/imatix/gsl.git
cd gsl/src
make
make install
```

<A name="toc3-74" title="Getting started" />
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

<A name="toc2-98" title="Setup your project environment" />
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

<A name="toc2-135" title="Configuration" />
## Configuration

zproject's `project.xml` contains an extensive description of the available configuration: The following snippet is taken from the `project.xml`:

```xml
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
        * vs2015

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
    <version major = "1" minor = "0" patch = "0" />

    <!--
        Specify which other projects this depends on.
        These projects must be known by zproject, and the list of
        known projects is maintained in the zproject_known_projects.xml model.
        You need not specify subdependencies if they are implied.
    <use project = "zyre" min_major= "1" min_minor = "1" min_patch = "0" />
    <use project = "uuid" optional= "1" implied = "1" />
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

    <!--
        Stuff that needs to be installed:

        NOTICE: If you copied this file to get started you want to delete or
                at least comment out those bin tag as they distribute the
                zproject files.

        * Linux -> /usr/local/bin
    -->
    <bin name = "zproject.gsl" />
    <bin name = "zproject_known_projects.xml" />

    <bin name = "zproject_actor.gsl" />
    <bin name = "zproject_android.gsl" />
    <bin name = "zproject_autoconf.gsl" />
    <bin name = "zproject_automake.gsl" />
    <bin name = "zproject_bench.gsl" />
    <bin name = "zproject_debian.gsl" />
    <bin name = "zproject_bindings_python.gsl" />
    <bin name = "zproject_bindings_qml.gsl" />
    <bin name = "zproject_bindings_qt.gsl" />
    <bin name = "zproject_bindings_ruby.gsl" />
    <bin name = "zproject_bindings_jni.gsl" />
    <bin name = "zproject_bindings_jni_vs20xx.gsl" />
    <bin name = "zproject_ci.gsl" />
    <bin name = "zproject_class.gsl" />
    <bin name = "zproject_class_api.gsl" />
    <bin name = "zproject_cmake.gsl" />
    <bin name = "zproject_cygwin.gsl" />
    <bin name = "zproject_docker.gsl" />
    <bin name = "zproject_docs.gsl" />
    <bin name = "zproject_git.gsl" />
    <bin name = "zproject_lib.gsl" />
    <bin name = "zproject_mkman.gsl" />
    <bin name = "zproject_mingw32.gsl" />
    <bin name = "zproject_nuget.gsl" />
    <bin name = "zproject_projects.gsl" />
    <bin name = "zproject_redhat.gsl" />
    <bin name = "zproject_tools.gsl" />
    <bin name = "zproject_vs2008.gsl" />
    <bin name = "zproject_vs20xx.gsl" />
    <bin name = "zproject_vs20xx_props.gsl" />

    <bin name = "mkapi.py" />
    <bin name = "fake_cpp" />
</project>
```

<A name="toc2-294" title="Sample API model" />
## Sample API model

The zproject scripts can also optionally generate the `@interface` in your class headers from an API model, in addition to a host of language bindings.  To opt-in to this behavior, just make a model to the `api` directory of your project.  For example, if your `project.xml` contains `<class name = "myclass"/>`, you could create the following `api/myclass.xml` file:

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

    <enum name = "mode">
        Enumeration defining different work modes. Constants are mandatory.
        <constant name="normal" constant = "1">
        <constant name="fast"   constant = "2">
        <constant name="safe"   constant = "3">
    </enum>

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
        <argument name = "conversion mode" type = "enum:myclass.mode">
            The container for this argument will get the following attributes:
            * `is_enum = 1"
            * `enum_class = "myclass"`
            * `enum_name = "mode"`
            * `c_type = "my_class_mode_t"`
        </argument>
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
```

<A name="toc3-516" title="Supported API Model Attributes" />
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

<A name="toc3-532" title="API Types" />
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

* "real" -- single-precision floating point.

* "buffer" -- byte array. To return a byte array, you should specify 'size' attribute that defines size. This can be a constant, 'size = "ZUUID_LEN"', or a dot followed by method name in the same class, e.g. 'size = ".size"'.

* "string" -- character array.

* "format" -- printf format, followed by zero or more arguments.

* "FILE", "va_list", "zmq_pollitem", "socket" -- literally that, in C. (Not sure if it is wise to use raw C types.)

* enumerations - to be reviewed as these have a specific syntax that crams multiple properties into one attribute, not our usual way of working.

* callbacks - tbd.

* Names of classes, e.g. zmsg.

<A name="toc3-573" title="Tips" />
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

<A name="toc3-590" title="Generate API model from C header files" />
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
python mkapi.py -I /path/to/your/pycparser/utils/fake_libc_include include/czmq.h
```

Note you must use top-level include as pycparser fails if it does not know any definition.

<A name="toc4-610" title="Known caveats" />
#### Known caveats

The tool can't distinguish methods which allocates new object. It does print a comment about adding fresh = "1" attribute to each method, which return non const pointer. However the final assigment must be done manually.

<A name="toc2-615" title="Language Binding Notes" />
## Language Binding Notes

<A name="toc3-618" title="JNI Language Binding" />
### JNI Language Binding

* Skips methods that it cannot handle properly.

* To build, you need gradle (or equivalent). Run 'gradle build jar' in the bindings/jni directory.
* To install, run 'gradle install'. This puts the files into $HOME/.m2/repository.

<A name="toc2-626" title="Draft API Support" />
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

<A name="toc2-658" title="Removal" />
## Removal

<A name="toc3-661" title="autotools" />
### autotools

```sh
make uninstall
```

<A name="toc2-668" title="Notes for Writing Language Bindings" />
## Notes for Writing Language Bindings

<A name="toc3-671" title="Schema/Architecture Overview" />
### Schema/Architecture Overview

* All `class`es SHALL be in the project model (`project.xml`).
* Each `class` MAY have a corresponding API model (`api/{class name}.xml`).
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

<A name="toc3-690" title="Informal Summary" />
### Informal Summary

A `class` is always the top-level entity in an API model, and it will be merged with the corresponding `class` entity defined in the project model. A class contains `method`s, `constructor`s, and `destructor`s (collectively, "method"s), and methods contain `argument`s and `return`s (collectively, "container"s). Each entity will contain both *semantic attributes* and *language-specific implementation attributes*.

<A name="toc3-695" title="Semantic Attributes" />
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
container.is_enum      # 0/1 (default: 0)
container.enum_name    # string if is_enum, otherwise undefined
container.enum_class   # string if is_enum, otherwise undefined
container.variadic     # 0/1 (default: 0)
container.va_start     # string - that holds the argment name for va_start ()
```

<A name="toc3-732" title="Language-Specific Implementation Attributes" />
### Language-Specific Implementation Attributes

Language-specific implementation attributes hold information that is not intrinsic to the concept of the container, but to the binding implementation.

In practice, language-specific attributes may contain any information that is useful to store as part of the container model to facilitate generation, according to any schema that is useful, but it may be helpful to try to follow patterns observed in other code generator scripts.

However, because the container is shared between all generators, which are run in an unspecified order, it's important that generators not rely on information resolved in generators. The one exceptions is that many generators will rely directly on information from the C implementation to which they bind.

It is also important that language-specific implementation attributes use a naming convention that avoids collisions. The easiest way to avoid collisions is to prefix all language-specific attributes with the name of the language, though in principle, any collision-free convention would be acceptable.

<A name="toc2-743" title="Ownership and License" />
## Ownership and License

The contributors are listed in AUTHORS. This project uses the MPL v2 license, see LICENSE.

zproject uses the [C4.1 (Collective Code Construction Contract)](http://rfc.zeromq.org/spec:22) process for contributions.

To report an issue, use the [zproject issue tracker](https://github.com/zeromq/zproject/issues) at github.com.

<A name="toc3-752" title="Hints to Contributors" />
### Hints to Contributors

Make sure that the project model hides all details of backend scripts. For example don't make a user enter a header file because autoconf needs it.

Do read your code after you write it and ask, "Can I make this simpler?" We do use a nice minimalist and yet readable style. Learn it, adopt it, use it.

Before opening a pull request read our [contribution guidelines](https://github.com/zeromq/zproject/blob/master/CONTRIBUTING.md). Thanks!

<A name="toc3-761" title="This Document" />
### This Document

This document is originally at README.txt and is built using [gitdown](http://github.com/imatix/gitdown).

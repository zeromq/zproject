.set GIT=https://github.com/zeromq/zproject
.sub 0MQ=ØMQ

# zproject - CLASS Project Generator

## Contents

.toc 2

## Overview

zproject is a community project, like most ZeroMQ projects, built using the C4.1 process, and licensed under MPL v2. It solves the Makefile problem really well. It is unashamedly for C, and more pointedly, for that modern C dialect we call CLASS. CLASS is the Minecraft of C: fun, easy, playful, mind-opening, and social. Read more about it [hintjens#79](http://hintjens.com/blog:79).

zproject grew out of the work that has been done to automatically generate the build environment in CZMQ. It allows to share these automations with other projects like [zyre](https://github.com/zeromq/zyre), [malamute](https://github.com/zeromq/malamute) or [hydra](https://github.com/edgenet/hydra) and at the same time keep everything in sync.

### Scope and Goals

zproject has these primary goals:

* generate cross-platform build environments.
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

## Tutorial

To understand step by step what zproject can do for you, read chapter 3 of
[@hintjens](https://github.com/hintjens) book [Scalable C](https://booksbyus.gitbooks.io/scalable-c/content/chapter3.html). Note that
the book is still work in progress!

## Installation

zproject uses the universal code generator called GSL to process its XML inputs
and create its outputs. Before you start you'll need to install GSL
(https://github.com/imatix/gsl) on your system.

```sh
git clone https://github.com/imatix/gsl.git
cd gsl/src
make
make install
```

GSL must be able to find the zproject resources on your system. Therefore you'll
need to install them. The following will install the zproject files to
`/usr/local/bin`.

```sh
git clone https://github.com/zeromq/zproject.git
cd zproject
./autogen.sh
./configure
make
make install
```

NB: You may need to use the `sudo` command when running `make install` to elevate your privileges, e.g.

```sh
sudo make install
```

NB: If you don't have superuser rights on a system you'll have to make sure zproject's gsl scripts can be found on your PATH.

## Getting started

### Setup your project environment

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

### Configuration

zproject's `project.xml` contains an extensive description of the available configuration: The following snippet is taken from the `project.xml`:

```xml
.pull project.xml
```

### Project dependencies

zproject's `use` element defines project dependencies.
Model is described in `zproject_known_projects.xml` file:

```xml
.pull zproject_known_projects.xml
```

### Optional : Class filename configuration

Exemple:
```classfilename
<classfilename use-cxx = "true" keep-tree = "true" pretty-print = "no" source-extension = "cpp" header-extension = "hpp" />
```

* use-cxx will force usage (or not) of c++.
* keep-tree will keeping the include tree on the install, must be used with a conservative name format (ex: pretty-print = "no"). Currently only supported with autotool.
* pretty-print define the type of class name format change in order to generate the filename. It use the pretty-print option of gsl (see Substituting Symbols and Expressions on https://github.com/imatix/gsl#expressions for more information).
* source-extension define the filename extension for source files in this project.
* header-extension define the filename extension for source files in this project.

Default value :
* pretty-print : substitute_non_alpha_to_make_c_identifier (c option)
* header-extension : h
* source-extension : c (unless a cc file is present, then cc)
* use-cxx : true if a cc file is present false otherwhise

### Targets

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

#### Target Options

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

#### Target Scopes

Each target works in its own copy of 'project'. It can therefore modify and extend 'project' as wanted, without affecting other targets.

### Modifying generated files in an already existent project

You may encounter a warning in a file you want to modify like this:
```
 ################################################################################
 #  THIS FILE IS 100% GENERATED BY ZPROJECT; DO NOT EDIT EXCEPT EXPERIMENTALLY  #
 #  Read the zproject/README.md for information about making permanent changes. #
 ################################################################################
```

If that happens, you need to follow these steps to make the modifications and then regenerate the code for czmq, malamute and zyre (all zeromq projects).

1. Prior making any changes, run the script tstgenbld.sh and save its output to a log file. This  will save the state of the world by regenerating several projects, building and running tests.
```sh
~/git/zproject$ ./tstgenbld.sh > ../before.log
```
2. Search for a specific string from the file in the zproject files (use *.*)
3. When you find it, make the modification in that file (most likely extensions will be .XML or .GSL)
4. Then execute these steps in a Linux machine to regenerate all files for your project. This will build, install and run tests on them again, after your changes have been made.
```sh
~/git/zproject$ ./tstgenbld.sh > ../after.log
~/git/zproject$ meld ../after.log ../before.log
```
4. Be aware that many files in the regenerated projects will change.
5. This also means you will need to commit changes on zproject (your mods) and in czmq, malamute, zyre (the regenerated files with your mods). From git documentation, it seems like the command "git add -uv" could help to find out what files were actually modified from all the files that were regenerated. Supposedly this will only add the ones that were actually modified, but you should double check them. Make sure to double check even line termination (or use a comparisson tool that flags those differences). Windows specific files should have (CR+LF) termination, while Linux specific should have (LF) only termination. Best is to look for ".terminator=" examples in existing .GSL files.

## API models

Using an API model zproject can generate the `@interface` section your class
headers. Further it allows zproject to generate various language bindings on top
of your CLASS project.

### Sample API model

All API models are placed into the `api` directory which resides in the root
directory of your project. For example, if your `project.xml` contains
`<class name = "myclass"/>`, you could create the following `api/myclass.api`
file:

```xml
.pull api/myclass.api
```

This model will cause the following `@interface` to be generated inside of
`include/myclass.h`. Note that if `include/myclass.h` has other handwritten
content outside of the `@interface` section this content will be retained. If
the header file does not exist zproject will create it.

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

For integer arguments you can specify one or more 'map' values, which a binding target can use to generate alternative methods. For example:

```xml
<argument name = "socket type" type = "integer">
    <map name = "PAIR" value = "ZMQ_PAIR" />
    <map name = "PUB"  value = "ZMQ_PUB" />
    <map name = "SUB"  value = "ZMQ_SUB" />
</argument>
```

The value should be a constant that the binding code has access to.

The following attributes are supported for arguments:

- `polymorphic` - indicates that the passed class instance is a `sockish` type. For an example see CZMQ's zsock class.

### API Types

This is an incomplete list of API types:

* "nothing" -- for return only, means "void" in C.

* "anything" -- means "void *" in C.

* "size" -- long size (64 bits), "size_t" in C.

* "time" -- long time (64 bits), "time_t" in C.

* "msecs" -- long number of msecs, "int64_t" in C.

* "file_size" -- long file size (64 bits).

* "boolean" -- Boolean.

* "byte" -- single octet.

* "char" -- single character (possibly multibyte, do we care?)

* "integer" -- 32-bit signed integer.

* "number" -- unsigned number, with 'size = "1|2|4|8"'.

* "real" -- single-precision floating point with 'size = "4"' (default) or double-precision with 'size = "8"'.

* "buffer" -- byte array. When passing a buffer argument, if the next argument has type 'size', the binding may fill the size automatically. To return a buffer, you should specify 'size' attribute that defines how to set the buffer size. This can be a constant, 'size = "ZUUID_LEN"', or a dot followed by method name in the same class, e.g. 'size = ".size"'.

* "string" -- character array.

* "sockish" -- a variant socket type, may be a zsock_t, libzmq void *, or an actor handle.

* "format" -- printf format, followed by zero or more arguments.

* "FILE", "va_list", "zmq_pollitem", "socket" -- literally that, in C. (Not sure if it is wise to use raw C types.)

* callbacks - tbd.

* Names of classes, e.g. zmsg.

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

#### Known caveats

The tool can't distinguish methods which allocates new object. It does print a comment about adding fresh = "1" attribute to each method, which return non const pointer. However the final assigment must be done manually.

## Language Binding Notes

### Java Language Binding

* Skips methods that it cannot handle properly.

* To build, you need gradle (or equivalent). Run 'gradle build jar' in the bindings/jni directory.
* To install, run 'gradle install'. This puts the files into $HOME/.m2/repository.

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

## Removal

### autotools

```sh
make uninstall
```

## Additional files
Installation of third party files is a *hard* problem. It is not platform
independent, became hard to maintain and impossible to use correctly. One of
zproject's goals is a simplicity. There is a simple installation model

### Design goals
* KISS, less configuration options the better
* no conditionals in the model, those SHALL be handled in background
* each option solves a REAL problem, avoid extending it because you can

### Example
```
    <main name = "MAIN">
        <install type = "systemd-tmpfiles" />
        <install type = "config" name = "MAIN-ldap-integration.cfg.example" />
    </main>
```

**systemd-tmpfiles**
This will add install information about systemd tmpfiles.d configuration files
to autotools, packaging, and so. The resulting file
/usr/lib/tmpfiles.d/MAIN.conf will be installed only if configure was called
with --with-systemd-units.

**config**
This will install additional configuration files to
$\(sysconfdir)/$\(project.name)/$\(name).

## Notes for Writing Targets

### Snippets

If you write a new target or extend one you might be in the situtation where you
need to put code fragments into files which are not specific to your target. For
example the `systemd` target has to extend files from the `autotools`, `debian`
and `redhat` targets. In order to keep those files as maintainable as possible
you'll include a snippet which is pull from your targets file. To include
a snippet call:

```
    insert_snippet (target)
```

Where target is the identifier for the insertion point i.e. the filename. To
register a snippet to be inserted simply call.

```
    register_snippet (target, name)
```

Target is must match the one in `insert_snippet` and the name identifies your
snippet. Then you can create a function or macro with the following form
(without the brackets):

```
    function snippet_<target>_<name>

    .macro snippet_<target>_<name>
```

This function will be called by the `insert_snippet` function. You can have an
arbitrary amount of registered snippets per insertion point which will be
inserted in arbitrary order so don't make any assumption on the order of the
snippets per insertion point.

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

### Informal Summary

A `class` is always the top-level entity in an API model, and it will be merged with the corresponding `class` entity defined in the project model. A class contains `method`s, `constructor`s, and `destructor`s (collectively, "method"s), and methods contain `argument`s and `return`s (collectively, "container"s). Each entity will contain both *semantic attributes* and *language-specific implementation attributes*.

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

## Ownership and License

The contributors are listed in AUTHORS. This project uses the MPL v2 license, see LICENSE.

zproject uses the [C4.1 (Collective Code Construction Contract)](http://rfc.zeromq.org/spec:22) process for contributions.

To report an issue, use the [zproject issue tracker](https://github.com/zeromq/zproject/issues) at github.com.

### Ownership and License of generated sources

The copyright of the output of zproject is by default property of the users. The license.xml file must be set up by the users to specify a license of their choosing.

### Hints to Contributors

Make sure that the project model hides all details of backend scripts. For example don't make a user enter a header file because autoconf needs it.

Do read your code after you write it and ask, "Can I make this simpler?" We do use a nice minimalist and yet readable style. Learn it, adopt it, use it.

Before opening a pull request read our [contribution guidelines](https://github.com/zeromq/zproject/blob/master/CONTRIBUTING.md). Thanks!

### This Document

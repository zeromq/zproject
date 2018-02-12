
# zproject - CLASS Project Generator

## Contents


**[Overview](#overview)**
*  [Scope and Goals](#scope-and-goals)

**[Tutorial](#tutorial)**

**[Installation](#installation)**

**[Getting started](#getting-started)**
*  [Setup your project environment](#setup-your-project-environment)
*  [Configuration](#configuration)
*  [Project dependencies](#project-dependencies)
*  [Optional : Class filename configuration](#optional--class-filename-configuration)
*  [Targets](#targets)
&emsp;[Target Options](#target-options)
&emsp;[Target Scopes](#target-scopes)
*  [Modifying generated files in an already existent project](#modifying-generated-files-in-an-already-existent-project)

**[API models](#api-models)**
*  [Sample API model](#sample-api-model)
*  [Supported API Model Attributes](#supported-api-model-attributes)
*  [API Types](#api-types)
*  [Tips](#tips)
*  [Generate API model from C header files](#generate-api-model-from-c-header-files)
&emsp;[Known caveats](#known-caveats)

**[Language Binding Notes](#language-binding-notes)**
*  [Java Language Binding](#java-language-binding)

**[Draft API Support](#draft-api-support)**

**[Removal](#removal)**
*  [autotools](#autotools)

**[Additional files](#additional-files)**
*  [Design goals](#design-goals)
*  [Example](#example)

**[Notes for Writing Targets](#notes-for-writing-targets)**
*  [Snippets](#snippets)

**[Notes for Writing Language Targets](#notes-for-writing-language-targets)**
*  [Schema/Architecture Overview](#schemaarchitecture-overview)
*  [Informal Summary](#informal-summary)
*  [Semantic Attributes](#semantic-attributes)

**[Ownership and License](#ownership-and-license)**
*  [Ownership and License of generated sources](#ownership-and-license-of-generated-sources)
*  [Hints to Contributors](#hints-to-contributors)
*  [This Document](#this-document)

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
        jenkins             Jenkins pipeline build
        mingw32             Mingw32 build system
        nuget               Packaging for NuGet
        python              Python binding
        qml                 QML binding
        qt                  Qt binding
        redhat              Packaging for RedHat
        ruby                Ruby binding
        travis              Travis CI scripts
            <option name="distcheck" value="0" /> will disable run of make distcheck in Travis CI
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
<project script = "zproject.gsl" name = "zproject"
    email = "zeromq-dev@lists.zeromq.org"
    license = "MPLv2"
    url = "https://github.com/zeromq/zproject"
    repository = "https://github.com/zeromq/zproject">

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
        Current libtool ABI version of your project's shared library.
        Start at 0:0:0 and see:
        http://www.gnu.org/software/libtool/manual/html_node/Updating-version-info.html
        for details on how/when to increment it.
        If not defined 0:0:0 will be used.
    <abi current = "0" revision = "0" age = "0" />
    -->

    <!--
        Specify which other projects this depends on.
        These projects must be known by zproject, and the list of
        known projects is maintained in the zproject_known_projects.xml model.
        You need not specify subdependencies if they are implied.
        Dependencies that support the autotools build system are automatically
        built by travis ci if you supply a git repository or a tarball URI.
        Set type to "runtime" to have the packages install-depend on it rather
        than build-depend (default type is "build").
        The travis ci will use the installed packages when building instead of
        rebuilding if available.
    <use project = "zyre" min_major= "1" min_minor = "1" min_patch = "0" />
    <use project = "czmq"
        min_major= "3" min_minor = "0" min_patch = "2"
        next_incompatible_major = "4"
        />
    <use project = "uuid" optional= "1" implied = "1" />
    <use project = "myfirstlib" repository = "http://myfirstlib.org/myfirstlib.git" />
    <use project = "mysecondlib" tarball = "http://mysecondlib.org/mysecondlib-1.2.3.tar.gz" />
    <use project = "lua-5.1" am_lib_macro = "LUA_5_1" tarball = "..." />
    -->

    <use project = "gsl" type = "runtime" />

    <!-- Header Files
         name := The name the header file to include without file ending
    <header name = "myproject_prelude" />
    -->

    <!--
        Classes, if the class header or source file doesn't exist, this will
        generate a skeletons for them.
        Use private = "1" for internal classes
        Use selftest = "0" to not generate selftest code
    <class name = "myclass">Public class description</class>
    <class name = "someother" private = "1">Private class description</class>
    -->

    <!--
        Actors, are built using the simple actor framework from czmq. If the
        actors class header or source file doesn't exist, this will generate a
        skeleton for them. The generated test method of the actor will teach
        you how to use them. Also have a look at the CZMQ docs to learn more
        about actors.
        Use selftest = "0" to not generate selftest code
    <actor name = "myactor">Public actor description</actor>
    <actor name = "someactor" private = "1">Private actor description</actor>
    -->

    <!--
        Main programs built by the project
                 use private = "1" for internal tools
    <main name = "progname">Exported public tool</main>
    <main name = "progname" private = "1">Internal tool</main>
    <main name = "progname" service = "1">Installed as system service, single-instance</main>
    <main name = "progname" service = "2">Installed as system service, multi-instance (@)</main>
    <main name = "progname" service = "3">Installed as system service, both single and multi-instance (@)</main>
    <main name = "progname" timer = "3">Installed as system timer unit, both single and multi-instance (@)</main>
    <main name = "progname" service = "1" timer = "1">Installed with both system timer and service units, single-instance - probably the former triggers the latter occasionally</main>
        Note that <bin> tags for secondary distributed programs (or scripts)
        now also support the service and timer attributes with same semantics.
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

    <target name = "obs" />
    <target name = "debian" />
    <target name = "redhat" />

    <!-- Note: zproject itself uses a customized CI-testing routine
         on Travis CI, not a generated one, so DO NOT ENABLE this one:
        <target name = "travis" />
    -->

    <!-- Jenkins target creates jenkins pipeline
         Pipeline file is not overwriten if it exists.

         Your projects can build under a docker container OR agents
         matched by a label OR under an "any" agent by default.
         If you specify a complex label expression, be sure to use
         XML escaping of the amperesand character (&amp;) if some of
         your tooling expects project.xml to be valid XML (the GSL
         parser accepts a verbatim amperesand character as well).

         The agent_single option is a flag that enables parallel
         builds of this component on several agents (specified by
         label or docker) vs. a sequential build on a single agent.

         Similarly, a check_sequential option can be defined so that
         self-testing stages would run sequentially. This can be needed
         at early stages of a project's evolution, where hardcoding is
         prevalent so parallel runs in same operating environemnt cause
         conflicts to each other. Ultimately a project should remove
         this flag ;)

         The build_* and test_* options influence the default setting
         of corresponding build arguments for the project. You can
         still run a custom Jenkins Build with Arguments with other
         checkboxes clicked, e.g. while developing a missing feature.
         If not explicitly set to 0, most of these options are assumed
         "true", as normally a project should be capable of all these
         aspects. Note however that a project with no classes marked
         "stable" would by default not test non-DRAFT builds as the
         configure.ac script would have no support for those anyway.

         The require_gitignore option (enabled by default) also causes
         the test to fail, rather than warn, if untracked or changed
         files are found as a result of some build or test stage.

         Also note, that after successful build and test steps, the
         job generated by this Jenkinsfile can optionally trigger
         some other job specific to your installation of a Jenkins
         server, to handle the deployment of tested code (whichever
         way you'd define that). For this optional feature, your
         Jenkins master should define (and propagate to its agents)
         the environment values DEFAULT_DEPLOY_BRANCH_PATTERN (regex)
         and DEFAULT_DEPLOY_JOB_NAME (note to start with a slash for
         absolute naming; jobs in a folder may use relative paths too).
         That job should accept parameters DEPLOY_GIT_URL (URL of repo),
         DEPLOY_GIT_BRANCH (name for decision-making), DEPLOY_GIT_COMMIT
         (actual commit to check out and shrink-wrap into packaging.

         The test_install check tries to "make DESTDIR=... install" where
         the DESTDIR is test_install_DESTDIR value (must be an absolute
         path), or BUILD_DIR/tmp/_inst if the option is unspecified/empty.

         The test_cppcheck is different, as it calls the "cppcheck" tool
         which may be not installed on a particular Jenkins deployment.
         The `make cppcheck` recipe is safe to call in either case, so by
         default this option is enabled if not set explicitly. Same idea
         goes for build_docs as it requires asciidoc and xmlto toolkits,
         except it is off by default to avoid churning CPUs with no tools.
         A further dist_docs enables preparation of a "dist" tarball from
         the workspace configured with docs, so you can forward it to the
         publishing helper job and avoid rebuilding manpages for packaging.

         The triggers_pollSCM option sets up the pipeline-generated job
         for regular polling of the original SCM repository, using the
         Jenkins cron syntax. The default is approximately every 5 minutes
         with a spread to minimize burst-loads vs quiet times. An explicit
         empty string disables polling, so you'd only run the job manually.
         Note that the most frequent working setting is "H/2", NOT a "H/1".

         The use_test_timeout option sets up the default timeout for test
         steps (further configurable at run-time as a build argument).
         Generally unit tests should not take pathologically long, so the
         default of 10 minutes should commonly suffice even for distchecks.
         If your selftests are known to take a lot of time, set this option.

         A use_test_retry option allows to retry each failing test step
         for the specified amount of attempts; it is deemed good if the
         test passes at least once. This option should not normally need
         to be used -- only if selftests somehow depend on environmental
         circumstances and fail occasionally but not always. Ultimately,
         project developers should find and fix the issue in tests (or in
         the production codebase) so it always works on the first try,
         bulletproof.

         As a workaround for some versions of Jenkins, if your project uses
         "weird" (generally non-ASCII) filenames in the build directory,
         their removal with Pipeline deleteDir() can fail even though it
         should not. If this bites you, set use_deleteDir_rm_first=1 in
         the project, so the OS native "rm" is tried first.

    <target name = "jenkins">
        <option name = "file" value = "Jenkinsfile" />
        <option name = "agent_docker" value = "zeromqorg/czmq" />
        <option name = "agent_label" value = "linux || macosx || bsd || solaris || posix || windows" />
        <option name = "agent_single" value = "1" />
        <option name = "check_sequential" value = "1" />
        <option name = "triggers_pollSCM" value = "H/5 * * * *" />
        <option name = "build_without_draft_api" value = "0" />
        <option name = "build_with_draft_api" value = "0" />
        <option name = "build_docs" value = "1" />
        <option name = "dist_docs" value = "1" />
        <option name = "require_gitignore" value = "0" />
        <option name = "use_deleteDir_rm_first" value = "1" />
        <option name = "use_test_timeout" value = "30" />
        <option name = "use_test_retry" value = "3" />
        <option name = "test_check" value = "0" />
        <option name = "test_memcheck" value = "0" />
        <option name = "test_distcheck" value = "0" />
        <option name = "test_install" value = "0" />
        <option name = "test_install_DESTDIR" value = "/tmp/proto-area" />
        <option name = "test_cppcheck" value = "1" />
    </target>
    -->
    <target name = "jenkins" >
        <option name = "agent_label" value = "linux || macosx || bsd || solaris || posix || windows" />
        <option name = "agent_single" value = "1" />
        <!-- Note: for zproject itself, all the *check jobs are
             essentially a loopback to distcheck itself -->
        <option name = "test_check" value = "1" />
        <option name = "test_memcheck" value = "0" />
        <option name = "test_distcheck" value = "0" />
        <option name = "test_cppcheck" value = "0" />
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
    <bin name = "zproject_jenkins.gsl" />
    <bin name = "zproject_lua_ffi.gsl" />
    <bin name = "zproject_mingw32.gsl" />
    <bin name = "zproject_nodejs.gsl" />
    <bin name = "zproject_nuget.gsl" />
    <bin name = "zproject_obs.gsl" />
    <bin name = "zproject_python.gsl" />
    <bin name = "zproject_python_cffi.gsl" />
    <bin name = "zproject_qml.gsl" />
    <bin name = "zproject_qt.gsl" />
    <bin name = "zproject_redhat.gsl" />
    <bin name = "zproject_rpi.gsl" />
    <bin name = "zproject_ruby.gsl" />
    <bin name = "zproject_systemd.gsl" />
    <bin name = "zproject_travis.gsl" />
    <bin name = "zproject_vagrant.gsl" />
    <bin name = "zproject_vs2008.gsl" />
    <bin name = "zproject_vs20xx.gsl" />
    <bin name = "zproject_vs20xx_props.gsl" />

    <bin name = "zproject_known_projects.xml" />
    <bin name = "mkapi.py" />
    <bin name = "fake_cpp" />
</project>
```

### Project dependencies

zproject's `use` element defines project dependencies.
Model is described in `zproject_known_projects.xml` file:

```xml
<known_projects>

    <!-- ZeroMQ Projects -->
    <!--
        Problem: naming style is inconsistent
        we sometimes use libxxx and sometimes xxx; the git repo name
        is unpredictable; sometimes we override with the prefix and
        sometimes with libname.

        Proposed solution: project name should always be git repo
        name; prefix and libname should always be specified. For
        compatibility we can define aliases. E.g.:

        Also, 'cmake name' is target specific and must go.

        Suggested model:
        <use
            project = "libzmq"          required
            master = "https://github.com/zeromq"
                                        required
            libname = "libzmq"          default = lib<prefix>
            prefix = "zmq"              default = project
            test = "zmq_init"           required same as AC_CHECK_LIB in autoconf
            release = "<tagname>"       default = "master"
            abi = "version"             default = "0:0:0"
            header = "<filename>"       default = <prefix>.h
            language = "C|C++"          default = "C"
            optional = "1"              default = "0"
            debian_name = "libzmq5-dev" default = lib<name>-dev
            redhat_name = "zeromq-devel" default = <name>-devel
                <add_config_opts>--with-dep1=nuance</add_config_opts>
                <add_config_opts>--enable-feature2</add_config_opts>
        </use>
    -->

    <use project = "libzmq" prefix = "zmq" debian_name = "libzmq3-dev" redhat_name = "zeromq-devel"
        repository = "https://github.com/zeromq/libzmq.git"
        test = "zmq_init" />

    <!-- Note: if your project requires an older CZMQ (e.g. if you need
        `release = "v3.0.2"`), you may need to `test = "zctx_test"`.
        Also note that you can instead require particular package
        version (as reported by pkg-config records). -->
    <use project = "czmq" libname = "libczmq"
        repository = "https://github.com/zeromq/czmq.git"
        test = "zhashx_test">
        <use project = "libzmq" />
    </use>

    <use project = "zyre" libname = "libzyre"
        repository = "https://github.com/zeromq/zyre.git"
        test = "zyre_test">
        <use project = "czmq" />
    </use>

    <use project = "malamute" libname = "libmlm"
        repository = "https://github.com/zeromq/malamute.git"
        header = "malamute.h"
        prefix = "mlm"
        test = "mlm_server_test">
        <use project = "libzmq" />
        <use project = "czmq" />
    </use>

    <use project = "gsl" libname = ""
        repository = "https://github.com/zeromq/gsl.git"
        debian_name = "generator-scripting-language"
        redhat_name = "generator-scripting-language">
    </use>

    <!-- Edgenet Projects -->

    <use project = "drops" libname = "libdrops"
        repository = "https://github.com/edgenet/drops.git"
        test = "drops_test">
        <use project = "czmq" />
        <use project = "zyre" />
    </use>

    <use project = "hydra" libname = "libhydra"
        repository = "https://github.com/edgenet/hydra.git"
        test = "hydra_server_test">
        <use project = "czmq" />
    </use>

    <!-- Various known third-party projects
        (If you're unsure of where a project belongs, add it here) -->

    <use project = "libsodium" prefix = "sodium"
        repository = "https://github.com/jedisct1/libsodium.git"
        release = "stable"
        test = "sodium_init" />

    <use project = "libcurl"
        repository = "https://github.com/curl/curl.git"
        test = "curl_easy_init"
        header = "curl/curl.h" />

    <use project = "editline"
        repository = "https://github.com/troglobit/editline.git"
        test = "readline" />

    <use project = "fuse"
        repository = "http://git.code.sf.net/p/fuse/fuse.git"
        test = "fuse_main" />

    <use project = "jansson"
        repository = "https://github.com/akheron/jansson.git"
        test = "json_object" />

    <use project = "jemalloc"
        repository = "https://github.com/jemalloc/jemalloc.git"
        test = "malloc"
        header = "jemalloc/jemalloc.h" />

    <use project = "msgpack"
        repository = "https://github.com/msgpack/msgpack-c.git"
        test = "msgpack_version" />

    <use project = "uuid"
        test = "uuid_generate"
        header = "uuid/uuid.h"
        redhat_name = "libuuid-devel"
        debian_name = "uuid-dev" />

    <use project = "asound"
        test = "snd_asoundlib_version"
        header = "alsa/asoundlib.h" />

    <use project = "zdb"
        repository = "https://bitbucket.org/tildeslash/libzdb.git"
        test = "ConnectionPool_start" />

    <use project = "json-c"
        header = "json-c/json.h"
        test = "json_object_to_json_string" />

    <use project = "libfastjson"
        repository = "https://github.com/rsyslog/libfastjson/"
        header = "libfastjson/json.h"
        test = "json_object_to_json_string" />

    <use project = "lognorm"
        repository = "https://github.com/rsyslog/liblognorm/"
        test = "ln_initCtx">
        <use project = "libfastjson" />
    </use>

    <use project = "zdiscgo"
        repository = "https://github.com/zeromq/zdiscgo.git"
        test = "zdiscgoplugin_new" />

    <use project = "systemd"
        libname = "libsystemd"
        prefix = "libsystemd"
        linkname = "systemd"
        header = "systemd/sd-daemon.h"
        test = "sd_listen_fds" />

    <use project = "protobuf-c"
         repository = "https://github.com/protobuf-c/protobuf-c/"
         test = "protobuf_c_version"
         header = "protobuf-c/protobuf-c.h"/>

    <!-- 42ITY project https://github.com/42ity https://42ity.org -->
    <use project = "fty-proto" libname = "libfty_proto" header="ftyproto.h"
        repository = "https://github.com/42ity/fty-proto"
        test = "fty_proto_test">
        <use project = "libzmq"/>
        <use project = "czmq"/>
        <use project = "malamute"/>
    </use>

    <!-- OS packagers make life hard by renaming the package, binaries and
         even library SONAMEs - so we have to guess a bit; note that for
         practical purposes, lua-5.2 suffices as lua-5.1 (if fixes happen
         to be needed, they are trivial and googlable) -->
    <use project = "lua-5.1" libname = "lua" prefix="lua"
        optional = "0" am_lib_macro = "LUA_5_1"
        min_major = "5" min_minor = "1" min_patch = "0"
        debian_name="liblua5.1-0-dev" redhat_name="lua-devel"
        test = "lua_close">
            <linkname>lua5.2</linkname>
            <linkname>lua52</linkname>
            <linkname>lua5.1</linkname>
            <linkname>lua51</linkname>
            <linkname>lua</linkname>
            <pkgconfig>lua5.2</pkgconfig>
            <pkgconfig>lua52</pkgconfig>
            <pkgconfig>lua5.1</pkgconfig>
            <pkgconfig>lua51</pkgconfig>
            <pkgconfig>lua</pkgconfig>
    </use>

    <use project = "lz4"
        libname = "liblz4"
        redhat_name = "liblz4-devel"
        header = "lz4.h"
        test = "LZ4_decompress_safe" />

</known_projects>
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
<class name = "myclass">
    <!--
        This model defines a public API for binding.

        It shows a language binding developer what to expect from the API XML
        files.
    -->
    My Feature-Rich Class

    <include filename = "license.xml" />

    <constant name = "default port" value = "8080">registered with IANA</constant>

    <constant name = "normal" value = "1" />
    <constant name = "fast"   value = "2" />
    <constant name = "safe"   value = "3" />

    <!-- Constructor is optional; default one has no arguments -->
    <constructor>
        Create a new myclass with the given name.
        <argument name = "name" type = "string" />
    </constructor>

    <!-- Destructor is optional; default one follows standard style -->
    <destructor>
        Destructors implicitly get a new argument prepended, which:

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
        <argument name = "default float" type = "real" />
        <argument name = "standard float" type = "real" size = "4" />
        <argument name = "standard double" type = "real" size = "8" />
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

_This documentation was generated from zproject/README.txt using [Gitdown](https://github.com/zeromq/gitdown)_

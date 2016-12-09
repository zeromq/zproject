#!/usr/bin/env bash
set -ex

mkdir tmp
BUILD_PREFIX=$PWD/tmp

CONFIG_OPTS=()
CONFIG_OPTS+=("CFLAGS=-I${BUILD_PREFIX}/include")
CONFIG_OPTS+=("CPPFLAGS=-I${BUILD_PREFIX}/include")
CONFIG_OPTS+=("CXXFLAGS=-I${BUILD_PREFIX}/include")
CONFIG_OPTS+=("LDFLAGS=-L${BUILD_PREFIX}/lib")
CONFIG_OPTS+=("PKG_CONFIG_PATH=${BUILD_PREFIX}/lib/pkgconfig")
CONFIG_OPTS+=("--prefix=${BUILD_PREFIX}")
CONFIG_OPTS+=("--with-docs=no")
CONFIG_OPTS+=("--quiet")

CMAKE_OPTS=()
CMAKE_OPTS+=("-DCMAKE_INSTALL_PREFIX:PATH=${BUILD_PREFIX}")
CMAKE_OPTS+=("-DCMAKE_PREFIX_PATH:PATH=${BUILD_PREFIX}")
CMAKE_OPTS+=("-DCMAKE_LIBRARY_PATH:PATH=${BUILD_PREFIX}/lib")
CMAKE_OPTS+=("-DCMAKE_INCLUDE_PATH:PATH=${BUILD_PREFIX}/include")

# Clone and build dependencies
echo "`date`: Starting build of dependencies: gsl..."
time git clone --quiet --depth 1 https://github.com/imatix/gsl.git gsl.git
cd gsl.git
git --no-pager log --oneline -n1
if [ -e autogen.sh ]; then
    time ./autogen.sh 2> /dev/null
fi
if [ -e buildconf ]; then
    time ./buildconf 2> /dev/null
fi
time ./configure "${CONFIG_OPTS[@]}"
time make -j4
time make install
cd ..

# Build and check this project
cd ../..
echo "`date`: Starting build of currently tested zproject..."
PKG_CONFIG_PATH=${BUILD_PREFIX}/lib/pkgconfig time cmake "${CMAKE_OPTS[@]}" .
time make all VERBOSE=1 -j4
time ctest -V
time make install

echo "`date`: Starting test of zproject (and gsl) by reconfiguring czmq..."
time git clone --depth 1 https://github.com/zeromq/czmq.git czmq.git
( cd czmq.git && \
  PATH=$PATH:${BUILD_PREFIX}/bin time ${BUILD_PREFIX}/bin/gsl -target:* project.xml \
) || exit 1
echo "`date`: Builds completed without fatal errors!"

echo "=== Are GitIgnores good after making zproject '$BUILD_TYPE'? (should have no output below)"
git status -s || true
echo "==="

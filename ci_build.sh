#!/usr/bin/env bash
set -x
set -e

if [ "$BUILD_TYPE" == "default" ]; then
    mkdir tmp
    BUILD_PREFIX=$PWD/tmp

    echo "`date`: Starting build of dependencies: gsl..."
    time git clone --depth 1 https://github.com/imatix/gsl.git gsl.git
    ( cd gsl.git/src && \
      time make -j4 && \
      DESTDIR=${BUILD_PREFIX} time make install \
    ) || exit 1

    echo "`date`: Starting build of zproject..."
    ( time ./autogen.sh && \
      PATH=$PATH:${BUILD_PREFIX}/bin time ./configure --prefix="${BUILD_PREFIX}" && \
      time make && \
      time make install \
    ) || exit 1

    echo "`date`: Starting test of zproject (and gsl) by reconfiguring czmq..."
    time git clone --depth 1 https://github.com/zeromq/czmq.git czmq.git
    ( cd czmq.git && \
      PATH=$PATH:${BUILD_PREFIX}/bin time ${BUILD_PREFIX}/bin/gsl -target:* project.xml \
    ) || exit 1
    echo "`date`: Builds completed without fatal errors!"
else
    pushd "./builds/${BUILD_TYPE}" && REPO_DIR="$(dirs -l +1)" time ./ci_build.sh || exit 1
fi

echo "=== Are GitIgnores good after making zproject '$BUILD_TYPE'? (should have no output below)"
git status -s || true
echo "==="

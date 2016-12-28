#!/usr/bin/env bash
set -x
set -e

if [ "$BUILD_TYPE" == "default" ]; then
    mkdir tmp
    BUILD_PREFIX=$PWD/tmp

    git clone --depth 1 https://github.com/imatix/gsl.git gsl
    ( cd gsl/src && \
      make -j4 && \
      DESTDIR=${BUILD_PREFIX} make install \
    ) || exit 1

    ( ./autogen.sh && \
      PATH=$PATH:${BUILD_PREFIX}/bin ./configure --prefix="${BUILD_PREFIX}" && \
      make && \
      make install \
    ) || exit 1

    git clone --depth 1 https://github.com/zeromq/czmq.git czmq
    ( cd czmq && \
      PATH=$PATH:${BUILD_PREFIX}/bin gsl -target:* project.xml \
    ) || exit 1
else
    pushd "./builds/${BUILD_TYPE}" && \
    REPO_DIR="$(dirs -l +1)" ./ci_build.sh \
    || exit 1
fi

echo "=== Are GitIgnores good after making zproject '$BUILD_TYPE'? (should have no output below)"
git status -s || true
echo "==="

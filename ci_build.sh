#!/usr/bin/env bash

#
# This script is used by travis ci to test updates for zproject itself:
# it builds a latest GSL, then zproject, and tests it by regenerating
# a stable consumer project (CZMQ) which is expected to pass well.
# Optionally speeds up the compilation steps using ccache (stashed).
#

set -x
set -e

if [ "$BUILD_TYPE" == "default" ]; then
    mkdir tmp
    BUILD_PREFIX="$PWD/tmp"

    CCACHE_PATH="$PATH"
    CCACHE_DIR="${HOME}/.ccache"
    export CCACHE_PATH CCACHE_DIR
    # ccache -s 2>/dev/null || true

    if ! ((command -v dpkg-query >/dev/null 2>&1 && dpkg-query --list generator-scripting-language >/dev/null 2>&1) || \
           (command -v brew >/dev/null 2>&1 && brew ls --versions gsl >/dev/null 2>&1)); then
        git clone --depth 1 https://github.com/imatix/gsl.git gsl
        ( cd gsl/src && \
          CCACHE_BASEDIR=${PWD} && \
          export CCACHE_BASEDIR && \
          make -j4 && \
          DESTDIR="${BUILD_PREFIX}" make install \
        ) || exit 1
    fi

    ( ./autogen.sh && \
      PATH="${BUILD_PREFIX}/bin:$PATH" && export PATH && \
      CCACHE_BASEDIR=${PWD} && \
      export CCACHE_BASEDIR && \
      ./configure --prefix="${BUILD_PREFIX}" && \
      make && \
      make install \
    ) || exit 1

    # Verify new zproject by regenerating CZMQ without (syntax/runtime) errors
    # Make sure to prefer use of just-built and locally installed copy of gsl
    git clone --depth 1 https://github.com/zeromq/czmq.git czmq
    ( PATH="${BUILD_PREFIX}/bin:$PATH"; export PATH; \
      cd czmq && \
      CCACHE_BASEDIR=${PWD} && \
      export CCACHE_BASEDIR && \
      gsl -target:* project.xml \
    ) || exit 1

    echo "=== How well did ccache help on this platform?"
    ccache -s 2>/dev/null || true
    echo "==="
else
    pushd "./builds/${BUILD_TYPE}" && \
    REPO_DIR="$(dirs -l +1)" ./ci_build.sh \
    || exit 1
fi

echo "=== Are GitIgnores good after making zproject '$BUILD_TYPE'? (should have no output below)"
git status -s || true
echo "==="

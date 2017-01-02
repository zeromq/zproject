#!/usr/bin/env bash
set -x
set -e

if [ "$BUILD_TYPE" == "default" ]; then
    mkdir tmp
    BUILD_PREFIX="$PWD/tmp"

    if ! ((command -v dpkg-query >/dev/null 2>&1 && dpkg-query --list generator-scripting-language >/dev/null 2>&1) || \
           (command -v brew >/dev/null 2>&1 && brew ls --versions gsl >/dev/null 2>&1)); then
        git clone --depth 1 https://github.com/imatix/gsl.git gsl
        ( cd gsl/src && \
          make -j4 && \
          DESTDIR="${BUILD_PREFIX}" make install \
        ) || exit 1
    fi

    ( ./autogen.sh && \
      PATH="${BUILD_PREFIX}/bin:$PATH" && export PATH && \
      ./configure --prefix="${BUILD_PREFIX}" && \
      make && \
      make install \
    ) || exit 1

    # Verify new zproject by regenerating CZMQ without (syntax/runtime) errors
    # Make sure to prefer use of just-built and locally installed copy of gsl
    git clone --depth 1 https://github.com/zeromq/czmq.git czmq
    ( PATH="${BUILD_PREFIX}/bin:$PATH"; export PATH; \
      cd czmq && \
      gsl -target:* project.xml \
    ) || exit 1
else
    pushd "./builds/${BUILD_TYPE}" && \
    REPO_DIR="$(dirs -l +1)" ./ci_build.sh \
    || exit 1
fi

echo "=== Are GitIgnores good after making zproject '$BUILD_TYPE'? (should have no output below)"
git status -s || true
echo "==="

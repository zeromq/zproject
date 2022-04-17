#!/usr/bin/env bash
set -e

# NOTE: This script is not standalone, it is included from project root
# ci_build.sh script, which sets some envvars (like REPO_DIR below).
[ -n "${REPO_DIR-}" ] || exit 1

# Set this to enable verbose profiling
[ -n "${CI_TIME-}" ] || CI_TIME=""
case "$CI_TIME" in
    [Yy][Ee][Ss]|[Oo][Nn]|[Tt][Rr][Uu][Ee])
        CI_TIME="time -p " ;;
    [Nn][Oo]|[Oo][Ff][Ff]|[Ff][Aa][Ll][Ss][Ee])
        CI_TIME="" ;;
esac

# Set this to enable verbose tracing
[ -n "${CI_TRACE-}" ] || CI_TRACE="no"
case "$CI_TRACE" in
    [Nn][Oo]|[Oo][Ff][Ff]|[Ff][Aa][Ll][Ss][Ee])
        set +x ;;
    [Yy][Ee][Ss]|[Oo][Nn]|[Tt][Rr][Uu][Ee])
        set -x ;;
esac

cd "${REPO_DIR}" || exit
PATH="`pwd`:$PATH"
export PATH

rm -rf tmp-deps
mkdir tmp-deps

echo "=== Install gitdown"
( cd tmp-deps && git clone https://github.com/zeromq/gitdown.git gitdown ) \
&& ( cd tmp-deps/gitdown && ./install-wrapper "${REPO_DIR}" ) || exit $?
command -v gitdown >/dev/null 2>&1

echo "=== Configure zproject to get a Makefile"
$CI_TIME ./autogen.sh && \
PATH="${BUILD_PREFIX}/bin:$PATH" && export PATH && \
CCACHE_BASEDIR=${PWD} && \
export CCACHE_BASEDIR && \
$CI_TIME ./configure --prefix="${BUILD_PREFIX}" || exit $?

echo "=== Make sure zproject markdown docs are up to date"
touch *.txt *.xml
make README.md
rm -f "${REPO_DIR}/gitdown"
if [[ $(git --no-pager diff -w) ]]; then
    git --no-pager diff -w
    echo "=== FAIL: There are diffs between current README.md and the one generated by gitdown!"
    exit 1
fi
if [[ $(git status -s) ]]; then
    git status -s
    echo "=== FAIL: gitdown generated new markup!"
    exit 1
fi

echo "=== All seems OK"

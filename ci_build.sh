#!/usr/bin/env bash

set -x

mkdir tmp
BUILD_PREFIX=$PWD/tmp

( ./autogen.sh && ./configure --prefix=${BUILD_PREFIX} && make && make install ) || exit 1

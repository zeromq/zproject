FROM ubuntu:trusty

MAINTAINER Benjamin Henrion <zoobab@gmail.com>

RUN apt-get update && \
    apt-get install -y uuid-dev build-essential git-core libtool unzip && \
    apt-get install -y autotools-dev autoconf automake pkg-config libkrb5-dev && \
    ROOTDIR=`pwd` && \
    mkdir -p /tmp/myproject && \
    cd /tmp/myproject && \
    cd $ROOTDIR && \
    ( ./autogen.sh; ./configure; make check; make install; ldconfig ) && \
    rm -rf /tmp/myproject

CMD ["myproject"]

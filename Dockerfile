FROM zeromqorg/gsl

MAINTAINER ZeroMQ community

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y -q
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q --force-yes build-essential autoconf automake libtool pkg-config

COPY . /tmp/zproject
WORKDIR /tmp/zproject
RUN mkdir -p /tmp/myproject && ( ./autogen.sh; ./configure; make; make install; ldconfig ) && \
    rm -rf /tmp/myproject

FROM zeromqorg/gsl

MAINTAINER ZeroMQ community

RUN apt-get install -y build-essential autoconf automake libtool pkg-config

COPY . /tmp/zproject
WORKDIR /tmp/zproject
RUN mkdir -p /tmp/myproject && ( ./autogen.sh; ./configure; make; make install; ldconfig ) && \
    rm -rf /tmp/myproject

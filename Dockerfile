FROM zeromqorg/gsl

MAINTAINER ZeroMQ community

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y -q
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q --force-yes build-essential autoconf automake libtool pkg-config

COPY packaging/docker/run_zproject.sh /usr/local/bin/run_zproject.sh

COPY . /tmp/zproject
RUN cd /tmp/zproject && ( ./autogen.sh; ./configure; make; make install; ldconfig ) && rm -rf /tmp/zproject
ENTRYPOINT ["run_zproject.sh"]

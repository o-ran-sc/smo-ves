# Copyright 2017 AT&T Intellectual Property, Inc
#  
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  
# http://www.apache.org/licenses/LICENSE-2.0
#  
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# What this is: A Dockerfile for building an OPFNV VES Agent container image.
#
# Status: this is a work in progress, under test.
#

FROM ubuntu:bionic

RUN mkdir /opt/ves

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get -y upgrade
# Required for kafka: default-jre zookeeperd python-pip kafka-python
# Required for building librdkafka:  git build-essential
# libpthread-stubs0-dev libssl-dev libsasl2-dev liblz4-dev
# (or libz-dev?)
# Required for building collectd: pkg-config
RUN apt-get update && apt-get install -y default-jre zookeeperd \
python-pip pkg-config git build-essential libpthread-stubs0-dev \
libssl-dev libsasl2-dev liblz4-dev libz-dev
RUN pip install kafka-python

# Build Kafka client
RUN mkdir /opt/ves/librdkafka
ADD librdkafka /opt/ves/librdkafka
RUN /bin/bash -c 'cd /opt/ves/librdkafka; ./configure --prefix=/usr; \
make; make install'

# Install VES Agent
RUN pip install pyaml

RUN mkdir /opt/ves/barometer
ADD barometer /opt/ves/barometer

COPY start.sh /opt/ves/start.sh
ENTRYPOINT ["/bin/bash", "/opt/ves/start.sh"]

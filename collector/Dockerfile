# Original work Copyright 2017-2018 AT&T Intellectual Property, Inc
# Modified work Copyright 2021 Xoriant Corporation

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
# What this is: A Dockerfile for building an OPFNV VES Collector container image.
#
# Status: this is a work in progress, under test.
#

FROM ubuntu:focal

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git curl python3 python3-pip

COPY pip.conf /etc/pip.conf

RUN pip3 install requests==2.28.1 jsonschema kafka-python gevent PyYAML

RUN mkdir -p /opt/smo/certs

# Clone VES Collector
RUN mkdir /opt/smo/evel-test-collector
ADD evel-test-collector /opt/smo/evel-test-collector


COPY start.sh /opt/smo/start.sh

ENTRYPOINT ["/bin/bash", "/opt/smo/start.sh"]

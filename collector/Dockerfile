# Copyright 2017-2018 AT&T Intellectual Property, Inc
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
# What this is: A Dockerfile for building an OPFNV VES Collector container image.
#
# Status: this is a work in progress, under test.
#

FROM ubuntu:xenial

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get -y upgrade
RUN apt-get update && apt-get install -y git python-pip python-jsonschema curl
RUN pip install requests pytz tzlocal

RUN mkdir /opt/ves

# copy VES Collector over to the Docker
RUN mkdir /opt/ves/evel-test-collector
ADD evel-test-collector /opt/ves/evel-test-collector

COPY Dashboard.json /opt/ves/Dashboard.json
COPY start.sh /opt/ves/start.sh
ENTRYPOINT ["/bin/bash", "/opt/ves/start.sh"]

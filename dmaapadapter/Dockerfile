# Copyright 2021 Xoriant Corporation
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

FROM ubuntu:focal

ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y iputils-ping
RUN ping -c 4 pypi.org
RUN ping -c 4 files.pythonhosted.org
RUN echo "151.101.0.223 pypi.org" >> /etc/hosts
RUN echo "199.232.253.63 files.pythonhosted.org" >> /etc/hosts
RUN echo "=========AFTER DNS OVERRIDE============="
RUN ping -c 4 pypi.org
RUN ping -c 4 files.pythonhosted.org
RUN apt-get install -y git curl python3 python3-pip

#RUN apt update
RUN apt-get install -y iproute2 net-tools host wget curl
RUN ip route
RUN ip addr
RUN ifconfig -a
RUN netstat -rnv
RUN cat /etc/resolv.conf 
RUN host pypi.org
RUN host files.pythonhosted.org
RUN wget --verbose https://pypi.org  
RUN wget --verbose https://files.pythonhosted.org

RUN pip3 install requests jsonschema kafka-python flask confluent-kafka


RUN mkdir /opt/smo

# Clone adapter folder
RUN mkdir /opt/smo/adapter
ADD adapter /opt/smo/adapter


COPY start.sh /opt/smo/start.sh
ENTRYPOINT ["/bin/bash", "/opt/smo/start.sh"]

#!/bin/bash
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
#. What this is: Startup script for the OPNFV VES Collector running under docker.
# the variables used below are now passed in as environmental variables
# from the docker run command.
cd /opt/ves
touch monitor.log

config_file="evel-test-collector/config/collector.conf"
schema_file=`grep -w schema_file $config_file | head -1 | cut -d "=" -f 2 | xargs`

echo  "schema_file = " $schema_file  > monitor.log
if [ "$schema_file" != "" ]; then
        if ! [ -e $schema_file ]; then
                echo "Schema file does not exists!" >> monitor.log
		exit
        fi
else
        echo "Schema file path is missing in config file!" >> monitor.log
	exit
fi

sed -i -- \
  "s~log_file = /var/log/att/collector.log~log_file = /opt/ves/collector.log~" \
  $config_file
sed -i -- "s/vel_domain = 127.0.0.1/vel_domain = $ves_host/g" \
  $config_file
sed -i -- "s/vel_port = 30000/vel_port = $ves_port/g" \
  $config_file
sed -i -- "s/vel_username =/vel_username = $ves_user/g" \
  $config_file
sed -i -- "s/vel_password =/vel_password = $ves_pass/g" \
  $config_file
sed -i -- "s~vel_path = vendor_event_listener/~vel_path = $ves_path~g" \
  $config_file
sed -i -- "s~vel_topic_name = example_vnf~vel_topic_name = $ves_topic~g" \
  $config_file
sed -i -- "/vel_topic_name = /a influxdb = $ves_influxdb_host:$ves_influxdb_port" \
  $config_file
sed -i -- "s/elasticsearch_domain =/elasticsearch_domain = $elasticsearch_domain/g" \
  $config_file
sed -i -- "s/data_storage =/data_storage = $data_storage/g" \
  $config_file
sed -i -- "s/kafka_second_port =/kafka_second_port = $kafka_host_2:$kafka_port_2/g" \
  $config_file
sed -i -- "s/kafka_topic =/kafka_topic = $kafka_topic/g" \
  $config_file

echo; echo $config_file
cat $config_file

if [ "$ves_loglevel" != "" ]; then
  python3 /opt/ves/evel-test-collector/code/collector/monitor.py \
    --config /opt/ves/evel-test-collector/config/collector.conf \
    --influxdb $ves_influxdb_host:$ves_influxdb_port \
    --section default > /opt/ves/monitor.log 2>&1
else
  python3 /opt/ves/evel-test-collector/code/collector/monitor.py \
    --config /opt/ves/evel-test-collector/config/collector.conf \
    --influxdb $ves_influxdb_host:$ves_influxdb_port \
    --section default
fi

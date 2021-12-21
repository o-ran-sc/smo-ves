#!/bin/bash
# Original work Copyright 2017 AT&T Intellectual Property, Inc
# Modified work Copyright 2021 Xoriant Corporation
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
#. What this is: Startup script for the OPNFV Agent running under docker.

echo "Trying to connect Kafka Broker.."
timeout 1m bash -c 'until printf "" 2>>/dev/null >>/dev/tcp/$agent_kafka_host/$agent_kafka_port; do sleep 2; done'
success=$?
if [ $success -eq 0 ]
        then
                echo "Kafka is up.."
        else
                echo "No Kafka found .. exiting container.."
                exit;
fi

echo "Trying to connect smo-collector.."
timeout 1m bash -c 'until printf "" 2>>/dev/null >>/dev/tcp/$smo_collector_host/$smo_collector_port; do sleep 2; done'
success=$?
if [ $success -eq 0 ]
        then
                echo "smo-collector is up.."
        else
                echo "No smo-collector found .. exiting container.."
                exit;
fi

echo "$agent_kafka_host $agent_kafka_host" >>/etc/hosts
echo "agent_kafka_host =$agent_kafka_host"
echo "*** /etc/hosts ***"
cat /etc/hosts

cd /opt/smo/barometer/3rd_party/collectd-agent-app/agent_app
cat <<EOF >agent_app_config.conf
[config]
Domain = $smo_collector_host
Port = $smo_collector_port
Path = $smo_collector_path
Directory_path = $smo_collector_directory_path
UseHttps = $smo_collector_https
Username = $smo_collector_user
Password = $smo_collector_pass
SendEventInterval = $agent_interval
ApiVersion = $smo_collector_version
KafkaPort = $agent_kafka_port
KafkaBroker = $agent_kafka_host
EOF

cat agent_app_config.conf
echo "agent_mode=$agent_mode"

if [[ "$loglevel" == "" ]]; then
  loglevel=ERROR
fi

python3 agent_app.py --events-schema=$agent_mode.yaml --loglevel $loglevel \
  --config=agent_app_config.conf

# Dump agent_app.log if the command above exits (fails)
echo "*** agent_app.log ***"
cat agent_app.log

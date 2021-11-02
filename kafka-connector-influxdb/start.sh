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
cd /opt/ves
touch monitor.log

config_file="influxdb-connector/config/influxdb_connector.conf"

sed -i -- "s/influxdb =/influxdb = $ves_influxdb_host:$ves_influxdb_port/g" \
  $config_file
sed -i -- "s/kafka_server =/kafka_server = $kafka_host_2:$kafka_port_2/g" \
  $config_file

echo; echo $config_file
cat $config_file

echo; echo "wait for InfluxDB API at $ves_influxdb_host:$ves_influxdb_port"
while ! curl http://$ves_influxdb_host:$ves_influxdb_port/ping ; do
  echo "InfluxDB API is not yet responding... waiting 10 seconds"
  sleep 10
done

echo; echo "setup veseventsdb in InfluxDB"
# TODO: check if pre-existing and skip
curl -X POST http://$ves_influxdb_host:$ves_influxdb_port/query \
  --data-urlencode "q=CREATE DATABASE veseventsdb"

if [ "$ves_loglevel" != "" ]; then
  python3 /opt/ves/influxdb-connector/code/influxdb_connector.py \
    --config /opt/ves/influxdb-connector/config/influxdb_connector.conf \
    --influxdb $ves_influxdb_host:$ves_influxdb_port \
    --section default > /opt/ves/monitor.log 2>&1
else
  python3 /opt/ves/influxdb-connector/code/influxdb_connector.py  \
    --config /opt/ves/influxdb-connector/config/influxdb_connector.conf \
    --influxdb $ves_influxdb_host:$ves_influxdb_port \
    --section default
fi

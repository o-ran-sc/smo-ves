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
cd /opt/smo
touch monitor.log

config_file="influxdb-connector/config/influxdb_connector.conf"

sed -i -- "s/influxdb =/influxdb = $smo_influxdb_host:$smo_influxdb_port/g" \
  $config_file
sed -i -- "s/kafka_server =/kafka_server = $smo_kafka_host:$smo_kafka_port/g" \
  $config_file

echo; echo $config_file
cat $config_file

echo; echo "wait for InfluxDB API at $smo_influxdb_host:$smo_influxdb_port"
STARTTIME=$(date +%s)
max_time=60
while ! curl http://$smo_influxdb_host:$smo_influxdb_port/ping ;
   do
     ELAPSED_TIME=$(($(date +%s) - $STARTTIME))
     if [ $ELAPSED_TIME -ge $max_time ]; then
        echo "InfluxDB API is not yet up after several attempts! Exiting from script."
        exit 1
     fi
     echo "InfluxDB API is not yet responding... waiting 10 seconds"
     sleep 10
   done
   echo "Done."
echo; echo "setup eventsdb in InfluxDB"
# TODO: check if pre-existing and skip
curl -X POST http://$smo_influxdb_host:$smo_influxdb_port/query \
  --data-urlencode "q=CREATE DATABASE eventsdb"

if [ "$loglevel" != "" ]; then
  python3 /opt/smo/influxdb-connector/code/influxdb_connector.py \
    --config /opt/smo/influxdb-connector/config/influxdb_connector.conf \
    --influxdb $smo_influxdb_host:$smo_influxdb_port \
    --section default > /opt/smo/monitor.log 2>&1
else
  python3 /opt/smo/influxdb-connector/code/influxdb_connector.py  \
    --config /opt/smo/influxdb-connector/config/influxdb_connector.conf \
    --influxdb $smo_influxdb_host:$smo_influxdb_port \
    --section default
fi

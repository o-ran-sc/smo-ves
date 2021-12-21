#!/bin/bash
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

cd /opt/smo

sleep 10

echo; echo "Wait for Grafana API to be active"
STARTTIME=$(date +%s)
max_time=60
while ! curl http://$smo_grafana_host:$smo_grafana_port/ping ;
   do
     ELAPSED_TIME=$(($(date +%s) - $STARTTIME))
     if [ $ELAPSED_TIME -ge $max_time ]; then
        echo "Grafana API is not yet up after several attempts! Exiting from script."
        exit 1
     fi
     echo "Grafana API is not yet responding... waiting 10 seconds"
     sleep 10
   done
   echo "Done."
echo; echo "add Events datasource to Grafana"


# TODO: check if pre-existing and skip
cat <<EOF >/opt/smo/grafana/datasource.json
{ "name":"Events",
  "type":"influxdb",
  "access":"direct",
  "url":"http://$smo_influxdb_host:$smo_influxdb_port",
  "password":"root",
  "user":"root",
  "database":"eventsdb",
  "basicAuth":false,
  "basicAuthUser":"",
  "basicAuthPassword":"",
  "withCredentials":false,
  "isDefault":false,
  "jsonData":null
}
EOF

curl -H "Accept: application/json" -H "Content-type: application/json" \
  -X POST -d @/opt/smo/grafana/datasource.json \
  http://$smo_grafana_auth@$smo_grafana_host:$smo_grafana_port/api/datasources

echo; echo "add VES dashboard to Grafana"

curl -H "Accept: application/json" -H "Content-type: application/json" \
  -X POST -d @/opt/smo/grafana/dashboard.json \
  http://$smo_grafana_auth@$smo_grafana_host:$smo_grafana_port/api/dashboards/db



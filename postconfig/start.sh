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

cd /opt/ves

sleep 10


echo; echo "Wait for Grafana API to be active"
STARTTIME=$(date +%s)
max_time=60
while ! curl http://$ves_grafana_host:$ves_grafana_port/ping ;
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
echo; echo "add VESEvents datasource to Grafana"


# TODO: check if pre-existing and skip
cat <<EOF >/opt/ves/grafana/datasource.json
{ "name":"VESEvents",
  "type":"influxdb",
  "access":"direct",
  "url":"http://$ves_influxdb_host:$ves_influxdb_port",
  "password":"root",
  "user":"root",
  "database":"veseventsdb",
  "basicAuth":false,
  "basicAuthUser":"",
  "basicAuthPassword":"",
  "withCredentials":false,
  "isDefault":false,
  "jsonData":null
}
EOF

curl -H "Accept: application/json" -H "Content-type: application/json" \
  -X POST -d @/opt/ves/grafana/datasource.json \
  http://$ves_grafana_auth@$ves_grafana_host:$ves_grafana_port/api/datasources

echo; echo "add VES dashboard to Grafana"

curl -H "Accept: application/json" -H "Content-type: application/json" \
  -X POST -d @/opt/ves/grafana/dashboard.json \
  http://$ves_grafana_auth@$ves_grafana_host:$ves_grafana_port/api/dashboards/db



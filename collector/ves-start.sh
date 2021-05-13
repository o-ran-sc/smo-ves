#!/bin/bash

# Script to run the ves project and its dependent containers 
# Maintainer shrinivas.joshi@xoriant.com 

#List of containers for this project

#collector -- Read the event received from ves-agent and write it to
#             influxdb
#grafana -- Read the events written by ves-collector in influxdb and
#           show the graphs on UI
#influxdb -- Store the events in DB sent by ves-agent

#Port allotment on host system for the micro services running in docker.

#Stop all containers if those are running accedently.

./ves-stop.sh

influx_port=3330
grafana_port=8880
vel_ves_port=9999

#Check Docker, collectd and git is installed on the VM

#get local ip address of VM from first interface


local_ip=`/sbin/ip -o -4 addr list | grep enp | head -n 1 | awk '{print $4}' | cut -d/ -f1`
echo -e "Binding VES Services to local ip address $local_ip \n "
echo ""
echo -e "--------------------------------------------------------------------\n"
#Spin influx DB
echo -e "Starting influxdb container on Local Port Number $influx_port. Please wait..\n"
docker run -d -p $influx_port:8086 -v $PWD/influxdb influxdb
if [ $? != 0 ]
then
    exit 1
fi

sleep 5 #Give some time to spin the container and bring service up
echo "Done."
echo""
echo -e "--------------------------------------------------------------------\n"
#Spin Grafana Cotainer
echo -e "Starting Grafana cotainer on Local port number $grafana_port. Please wait..\n"
docker run -d -p $grafana_port:3000 grafana/grafana
if [ $? != 0 ]
then
    exit 1
fi
sleep 5 #Give some time to spin the container and bring service up
echo "Done."
echo ""
echo -e "--------------------------------------------------------------------\n"
echo ""
echo -e "--------------------------------------------------------------------\n"
#Spin collector container.
echo -e "Starting ves collector container on Local port number $vel_ves_port. Please wait\n"
docker run -d -e ves_influxdb_host=$local_ip \
       -e ves_influxdb_port=$influx_port -e ves_grafana_host=$local_ip \
       -e ves_grafana_port=$grafana_port -e ves_host=$local_ip \
       -e ves_port=$vel_ves_port -e ves_grafana_auth='admin:admin' \
       -e ves_user='user' -e ves_pass='password' -e ves_path=''\
       -e ves_topic='events' -e ves_loglevel='DEBUG' \
       -p $vel_ves_port:$vel_ves_port ves-collector
if [ $? != 0 ]
then
    exit 1
fi
sleep 6
echo "Done."
echo ""
echo""
echo -e "ves stack summary\n"

echo -e "===================================================================================================================\n"
echo ""
echo -e "ves collector listner port: $vel_ves_port \n"
echo -e "Grafana port: $grafana_port \n"
echo -e "To access grafana dashboard paste url  http://$local_ip:$grafana_port in web browser. "
echo -e "Grafana username/password is admin/admin *** DO NOT CHANGE THE ADMIN PASSWORD, CLICK SKIP OPTION ***\n"
echo ""
echo -e "===================================================================================================================\n" 

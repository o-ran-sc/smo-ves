#!/bin/bash

# Script to build ves project and its dependent containers 
# Maintainer shrinivas.joshi@xoriant.com 

#List of containers for this project

#ves-kafka -- kafka broker to store events recieved from collectd or other similar services
#ves-agent -- read events forom kafka and send those events to VEL port on ves-collector container
#ves-collector -- Read the event received from ves-agent and write it to influxdb
#grafana -- Read the events written by ves-collector in influxdb and show the graphs on UI
#influxdb -- Store the events in DB sent by ves-agent
#kafdrop -- UI for Kafka


#Port allotment on host system for the micro services running in docker.

#influx port 3330
#grafana port 8880
#kafka port 9092
#kafdrop 9000 
#zookeeper port 2181 2888 3888 8080
#VES port 9999
#Check Collectd and Docker is installed.

#Stop all containers if those are running accedently.

./ves-stop.sh

influx_port=3330
grafana_port=8880
kafka_port=9092 
kafdrop_port=9000
zookeeper_port=2181 
vel_ves_port=9999

OS=`uname -s`
# Check Docker, collectd, ip and git is installed on the VM

if ! which docker > /dev/null; then
   echo -e "Docker not found, please install docker from https://docs.docker.com/engine/install/ubuntu\n"
   exit;
fi

if ! which collectd > /dev/null; then
    if [ $OS = 'Darwin' ]
    then
	echo -e "Collectd not found, please install collectd using brew install collectd\n"
    elif [ $OS = 'Linux' ]
    then
	echo -e "Collectd not found, please install collectd using sudo apt-get install -y collectd\n"
    else
	echo -e "Could not determine kind of system. Collectd not found, please install collectd using whatever method works.\n"
    fi
   exit;
fi

if ! which ip > /dev/null; then
    if [ $OS = 'Darwin' ]
    then
	echo -e "ip not found, please install ip using brew install ip.\n"
    elif [ $OS = 'Linux' ]
    then
	echo -e "/sbin/ip not found, please install ip using sudo apt-get install ip.\n"
    else
	echo -e "Could not determine kind of system. ip not found, please install ip using whatever method works.\n"
	exit 1
    fi
   exit;
fi

clear

#get local ip address of VM from first interface
if [ $OS = 'Darwin' ]
then
    local_ip=`ip -4 addr list | grep en11 | grep inet | awk '{print $2}' | cut -d/ -f1`  
elif [ $OS = 'Linux' ]
then
    local_ip=`/sbin/ip -o -4 addr list | grep enp | head -n 1 | awk '{print $4}' | cut -d/ -f1`
else
    echo -e "Could not determine which OS this.\n"
    exit 1
fi
echo -e "Binding VES Services to local ip address $local_ip \n "
echo ""
echo -e "--------------------------------------------------------------------\n"
#Spin influx DB
echo -e "Starting influxdb container on Local Port Number $influx_port. Please wait..\n"
docker run -d -p $influx_port:8086 -v $PWD/influxdb influxdb:1.8.5
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
#Spin zookeeper container
echo -e "Starting zookeeper container on Local port number $zookeeper_port. Please wait..\n"
docker run -d --add-host mykafka:$local_ip --add-host myzoo:$local_ip \
       -p $zookeeper_port:2181 -p 2888:2888 -p 3888:3888 \
       -p 8800:8080 zookeeper
if [ $? != 0 ]
then
    exit 1
fi
sleep 5
echo "Done."
echo ""
echo -e "--------------------------------------------------------------------\n"
#Spin Kafka container.
echo -e "Starting Kafka container on Local port number $kafka_port. Please wait..\n"
docker run -d --add-host mykafka:$local_ip -e zookeeper_host=$local_ip \
       -e zookeeper_hostname='myzoo' -e zookeeper_port=$zookeeper_port \
       -e kafka_hostname='mykafka' -e kafka_port=$kafka_port \
       -p $kafka_port:$kafka_port ves-kafka
if [ $? != 0 ]
then
    exit 1
fi
sleep 7
echo "Done."
echo ""
echo -e "--------------------------------------------------------------------\n"
#Spin Kafdrop UI container (this is optional componant)
echo -e "Starting kafdrop UI container on Local port numner $kafdrop_port. please wait..\n"
docker run -d --add-host mykafka:$local_ip -p $kafdrop_port:9000 \
       -e KAFKA_BROKERCONNECT=$local_ip:$kafka_port \
       -e JVM_OPTS="-Xms64M -Xmx128M" obsidiandynamics/kafdrop:latest
if [ $? != 0 ]
then
    exit 1
fi
sleep 5
echo "Done."
echo ""
echo -e "--------------------------------------------------------------------\n"
# Spin ves-collector container.
echo -e "Starting ves collector container on Local port number $vel_ves_port. Please wait\n"
docker run -d -e ves_influxdb_host=$local_ip \
       -e ves_influxdb_port=$influx_port -e ves_grafana_host=$local_ip \
       -e ves_grafana_port=$grafana_port -e ves_host='localhost' \
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
echo -e "--------------------------------------------------------------------\n"
#Spin ves agent container.
echo -e "Starting ves agent container. Please wait\n" 
docker run -d -e ves_kafka_host=$local_ip \
       -e ves_kafka_hostname='mykafka' -e ves_host=$local_ip \
       -e ves_port=$vel_ves_port -e ves_path='' \
       -e ves_topic='events' -e ves_https='False' -e ves_user='user' \
       -e ves_pass='password' -e ves_interval='10' \
       -e ves_kafka_port=$kafka_port -e ves_mode='./yaml/host' \
       -e ves_version='7' -e ves_loglevel='DEBUG' ves-agent
if [ $? != 0 ]
then
    exit 1
fi
sleep 5
echo "Done."
echo ""
echo -e "--------------------------------------------------------------------\n"
echo""
echo -e "ves stack summary\n"
echo -e "===================================================================================================================\n"
echo ""
echo -e "Kafka port: $kafka_port \n"
echo -e "Kafdrop port: $kafdrop_port \n"
echo -e "ves collector listner port: $vel_ves_port \n"
echo -e "Grafana port: $grafana_port \n"
echo -e "To access kafdrop UI use http://$local_ip:$kafdrop_port from your web browser. \n"
echo -e "To access grafana dashboard paste url  http://$local_ip:$grafana_port in web browser. "
echo -e "Grafana username/password is admin/admin *** DO NOT CHANGE THE ADMIN PASSWORD, CLICK SKIP OPTION ***\n"
echo ""
echo -e "===================================================================================================================\n" 


#!/bin/bash

# Read configuration files
NEXUS_REPO=`release-1.0.0`
ARTIFACTS_VERSION=`1.1.0-SNAPSHOT`
DNS_IP_ADDR=$(cat /opt/config/dns_ip_addr.txt)
CLOUD_ENV=$(cat /opt/config/cloud_env.txt)
GERRIT_BRANCH=$(cat /opt/config/gerrit_branch.txt)
MTU=$(/sbin/ifconfig | grep MTU | sed 's/.*MTU://' | sed 's/ .*//' | sort -n | head -1)

# Add host name to /etc/host to avoid warnings in openstack images
if [[ $CLOUD_ENV != "rackspace" ]]
then
        echo 127.0.0.1 $(hostname) >> /etc/hosts

        # Allow remote login as root
        mv /root/.ssh/authorized_keys /root/.ssh/authorized_keys.bk
        cp /home/ubuntu/.ssh/authorized_keys /root/.ssh
fi

# Set private IP in /etc/network/interfaces manually in the presence of public interface
# Some VM images don't add the private interface automatically, we have to do it during the component installation
if [[ $CLOUD_ENV == "openstack_nofloat" ]]
then
        LOCAL_IP=$(cat /opt/config/local_ip_addr.txt)
        CIDR=$(cat /opt/config/oam_network_cidr.txt)
        BITMASK=$(echo $CIDR | cut -d"/" -f2)

        # Compute the netmask based on the network cidr
        if [[ $BITMASK == "8" ]]
        then
                NETMASK=255.0.0.0
        elif [[ $BITMASK == "16" ]]
        then
                NETMASK=255.255.0.0
        elif [[ $BITMASK == "24" ]]
        then
                NETMASK=255.255.255.0
        fi

        echo "auto eth1" >> /etc/network/interfaces
        echo "iface eth1 inet static" >> /etc/network/interfaces
        echo "    address $LOCAL_IP" >> /etc/network/interfaces
        echo "    netmask $NETMASK" >> /etc/network/interfaces
        echo "    mtu $MTU" >> /etc/network/interfaces
        ifup eth1
fi

# Download dependencies
add-apt-repository -y ppa:openjdk-r/ppa
apt-get update
apt-get install -y apt-transport-https ca-certificates wget make openjdk-8-jdk git ntp ntpdate

# Download scripts from Nexus
curl -k $NEXUS_REPO/org.openecomp.demo/boot/$ARTIFACTS_VERSION/mr_vm_init.sh -o /opt/mr_vm_init.sh
curl -k $NEXUS_REPO/org.openecomp.demo/boot/$ARTIFACTS_VERSION/mr_serv.sh -o /opt/mr_serv.sh
chmod +x /opt/mr_vm_init.sh
chmod +x /opt/mr_serv.sh
mv /opt/mr_serv.sh /etc/init.d
update-rc.d mr_serv.sh defaults

# Download and install docker-engine and docker-compose
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-get install -y --allow-unauthenticated docker-engine

mkdir /opt/docker
curl -L https://github.com/docker/compose/releases/download/1.9.0/docker-compose-`uname -s`-`uname -m` > /opt/docker/docker-compose
chmod +x /opt/docker/docker-compose

# Set the MTU size of docker containers to the minimum MTU size supported by vNICs. OpenStack deployments may need to know the external DNS IP
if [ -s /opt/config/external_dns.txt ]
then
        echo "DOCKER_OPTS=\"--dns $(cat /opt/config/external_dns.txt) --mtu=$MTU\"" >> /etc/default/docker
else
        echo "DOCKER_OPTS=\"--mtu=$MTU\"" >> /etc/default/docker
fi

cp /lib/systemd/system/docker.service /etc/systemd/system
sed -i "/ExecStart/s/$/ --mtu=$MTU/g" /etc/systemd/system/docker.service
service docker restart

# DNS IP address configuration
echo "nameserver "$DNS_IP_ADDR >> /etc/resolvconf/resolv.conf.d/head
resolvconf -u

# Clone Gerrit repository and run docker containers
cd /opt
git clone -b $GERRIT_BRANCH --single-branch http://gerrit.onap.org/r/dcae/demo/startup/message-router.git dcae-startup-vm-message-router
./mr_vm_init.sh

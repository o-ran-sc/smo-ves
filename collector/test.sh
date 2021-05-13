#!/bin/bash

detect_interface=`ip link | awk -F: '$0 !~ "lo|vir|docker|^[^0-9]"{print $2a}' | awk 'BEGIN { ORS = " " } { print }'`
[ -z "$detect_interface" ] && echo -e "No usable network interface found.. exiting.. \n" && exit

detect_interface=`echo $detect_interface | sed 's/ *$//g'`
[ ! -z "$detect_interface" ] && echo "Interfaces found $detect_interface"

interface=`echo $detect_interface | cut -d " " -f 1`
echo -e "Using interface $interface for VES. \n"

echo $interface


.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

smo/ves Overview
================

Introduction

This repository supports the VES collector interface in O-RAN. It
makes use of three containers, the ves-collector container that
collects VES events posted by other parts of the O-RAN solution,
Grafana, which is used to display measurement (PM) data posted
by other entities and InfluxdB which is used to persist the data
received by the collector.

Prerequisites:

The prerequisites for using this solution are that you need Docker and docker-compose
installed on the machine, where you want to run these containers.

Build:

To build the solution, you need to do the following in the current
folder::

    % make

Run:

To run the solution, you need to invoke the following command::

    % docker-compose up -d ves-collector
    % docker-compose up -d ves-agent

or simply by the following make command::

    % make run

To stop the solution the following command should be invoked::

    % docker-compose down -d ves-collector
    % docker-compose down -d ves-agent

or simply by the following make command::

    % make stop


Following steps are required to install a certificate.
------------------------------------------------------
Self-Signed Certificates
~~~~~~~~~~~~~~~~~~~~~~~~
Following steps are required for self-signed certificate.
1. Create ves-certificate directory on the host system using command "mkdir ~/ves-certificate".
2. Go to ves-certificate directory and use below commands to create self-signed certificate files::

    openssl genrsa -out vescertificate.key 2048
    openssl req -new -key vescertificate.key -out vescertificate.csr
    openssl x509 -req -days 365 -in vescertificate.csr -signkey vescertificate.key -out vescertificate.crt
    
Third Party Certificates
~~~~~~~~~~~~~~~~~~~~~~~~
Third party certificates can be installed by overwriting the file *vescertificate.csr*, *vescertificate.key*, and *vescertficate.crt* in ~/ves-certificate directory of the host system.


Following steps are required to add an entry in the host file
-------------------------------------------------------------
Add following entry in host file on the computer from which user want to access Grafana  dashboard.
<IP Address of VM/Machine on which docker containers are running> smo-influxdb

For Example- Docker container running on the guest VM or different/remote machine having IP Address 192.168.56.110 then host file entry is as follows::

   192.168.56.110 smo-influxdb


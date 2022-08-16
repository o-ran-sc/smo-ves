.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0



Installation Guide
==================

.. contents::
   :depth: 3
   :local:

Abstract
--------

This document describes how to install smo-ves, it's dependencies and required system resources.


Version history

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2022-Aug-10        | 0.1.0              |  Santanu De        |  First draft       |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
|                    |                    |                    |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
|                    |                    |                    |                    |
|                    |                    |                    |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+


Introduction
------------

.. <INTRODUCTION TO THE SCOPE AND INTENTION OF THIS DOCUMENT AS WELL AS TO THE SYSTEM TO BE INSTALLED>


This document describes the supported software and hardware configurations for the reference component as well as providing guidelines on how to install and configure such reference system.

The audience of this document is assumed to have good knowledge in RAN network, Ubuntu 20.04 LTS Desktop Edition system and Docker Compose.


Preface
-------
.. <DESCRIBE NEEDED PREREQUISITES, PLANNING, ETC.>

Before starting the installation of smo-ves, make sure docker-compose, git are installed on the system

.. <note any preperation you need before setting up sotfware and hardware >


Hardware Requirements
---------------------
.. <PROVIDE A LIST OF MINIMUM HARDWARE REQUIREMENTS NEEDED FOR THE INSTALL>


Following minimum hardware requirements must be met for installation of smo-ves:

+--------------------+----------------------------------------------------+
| **HW Aspect**      | **Requirement**                                    |
|                    |                                                    |
+--------------------+----------------------------------------------------+
| **# of servers**   | 	1	                                          |
+--------------------+----------------------------------------------------+
| **CPU**            | 	4 core					          |
|                    |                                                    |
+--------------------+----------------------------------------------------+
| **RAM**            | 	8 GB minimum, 16 GB recommended			  |
|                    |                                                    |
+--------------------+----------------------------------------------------+
| **Disk**           | 	100 GB minimum, 500 GB recommended		  |
|                    |                                                    |
+--------------------+----------------------------------------------------+
| **NICs**           | 	1						  |
|                    |                                                    |
|                    | 							  |
|                    |                                                    |
|                    |  					 	  |
|                    |                                                    |
+--------------------+----------------------------------------------------+



Software Installation and Deployment
------------------------------------
.. <DESCRIBE THE FULL PROCEDURES FOR THE INSTALLATION OF THE O-RAN COMPONENT INSTALLATION AND DEPLOYMENT>

This section describes the installation of the smo-ves installation on the reference hardware.

Build
~~~~~

To build the solution, you need to do the following in the current folder::

   % docker-compose build

Run
~~~

To run the solution, you need to invoke the following command::

    % docker-compose up -d


To stop the solution the following command should be invoked::

    % docker-compose down



Following steps are required to install a certificate.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   
Self-Signed Certificates
^^^^^^^^^^^^^^^^^^^^^^^^
Following steps are required for self-signed certificate.
1. Create ves-certificate directory on the host system using command "mkdir ~/ves-certificate".
2. Go to ves-certificate directory and use below commands to create self-signed certificate files::

    openssl genrsa -out vescertificate.key 2048
    openssl req -new -key vescertificate.key -out vescertificate.csr
    openssl x509 -req -days 365 -in vescertificate.csr -signkey vescertificate.key -out vescertificate.crt

Third Party Certificates
^^^^^^^^^^^^^^^^^^^^^^^^
Third party certificates can be installed by overwriting the file *vescertificate.csr*, *vescertificate.key*, and *vescertficate.crt* in ~/ves-certificate directory of the host system.


Following steps are required to add an entry in the host file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add following entry in host file on the computer from which user want to access Grafana  dashboard.
<IP Address of VM/Machine on which docker containers are running> smo-influxdb

For Example- Docker container running on the guest VM or different/remote machine having IP Address 192.168.56.110 then host file entry is as follows::

    192.168.56.110 smo-influxdb




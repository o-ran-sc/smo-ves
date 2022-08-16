.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) <optionally add copywriters name>


User Guide
==========

This is the user guide for OSC smo/ves

.. contents::
   :depth: 3
   :local:
   
Check Containers  
----------------
Run the below command to status of the containers. All contaiers should be is "Up" state except "smo-post-config"::

 % docker-compose ps
 
Check VES API
-------------
Launch a browser and navigate to https://<IP Address of VM/Machine on which docker containers are running>:9999/v7/events/
 
 
Check DMAAP API
---------------
Launch a browser and navigate to http://<IP Address of VM/Machine on which docker containers are running>:5000/dmaapapi/v1/topics
 

Check Grafana Dashborad
-----------------------
Open http://<IP Address of VM/Machine on which docker containers are running>:3000/ in a browser. admin/admin is default username/password. No need to reset password. After login, visit Dashborads > Manage section. "Events Demo" Dashbaord is ready to use.  

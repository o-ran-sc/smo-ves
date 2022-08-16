.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


Release-Notes
=============


This document provides the release notes for F-RELEASE of semo-ves.

.. contents::
   :depth: 3
   :local:


Version history
---------------

+--------------------+--------------------+--------------------+--------------------+
| **Date**           | **Ver.**           | **Author**         | **Comment**        |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
| 2022-07-15         | 5.0.1              |                    | First version      |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
|                    |                    |                    |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+
|                    |                    |                    |                    |
|                    |                    |                    |                    |
+--------------------+--------------------+--------------------+--------------------+


Summary
-------

The O1/VES interface received a number of features and capabilities in this edition. Adding functional test cases, integrating with the Jenkins server, saving container images in the Nexus repository, enhancing the quality of the code, implementing CLM and Sonar Jobs, etc.



Release Data
------------

+--------------------------------------+--------------------------------------+
| **Project**                          | SMO VES      		              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo**                             | Repo: smo/ves                        |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | f-release                            |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | 2022-07-15                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | 	 		     	      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+




Feature Additions
^^^^^^^^^^^^^^^^^
**JIRA BACK-LOG:**

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-57	                       | Add Jenkins jobs for the smo repo    |
|                                      | 				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-55                               | Add dmaap and influx-db adapter      |
|                                      | plugins to the release process       |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-53                               | Remove redundant code in smo 	      |
|                                      | collector  			      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-68                               | Create CLM job for smo-ves project   |
|                                      |  				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-58                               | Add unit test cases in smo/ves       |
|                                      |  				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-64                               | Add smo-post-config image to         |
|                                      | the release process		      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+



Bug Corrections
^^^^^^^^^^^^^^^

**JIRA TICKETS:**

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-63 	                       | Modify configuration of              |
|                                      | Influxdb container		      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
^^^^^^^^^^^^

Software Deliverables
+++++++++++++++++++++

Complied container images are available at Nexus repository https://nexus3.o-ran-sc.org/. Search with keyword 'smo'.


Documentation Deliverables
++++++++++++++++++++++++++

Documentation is available at https://docs.o-ran-sc.org/projects/o-ran-sc-smo-ves/en/latest/release-notes.html




Known Limitations, Issues and Workarounds
-----------------------------------------

System Limitations
^^^^^^^^^^^^^^^^^^
Not identified



Known Issues
^^^^^^^^^^^^


**JIRA TICKETS:**

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| 		                       | 				      |
|     SMO-74                           | Failure of Sonar job 		      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| 	                               |  				      |
|                                      |  				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Workarounds
^^^^^^^^^^^
Working with the support team of the Linux Foundation to fix the problem.






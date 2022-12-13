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
| 2022-12-15         | 6.0.3              |                    | First version      |
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
| **Release designation**              | g-release                            |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | 2022-12-15                           |
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
| SMO-76	                       | Implement Standard Defined Validator |
|                                      | 				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-86                               | Modify docker images release plan    |
|                                      | 				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-89                               | Introduce requirements.txt file in   |
|                                      | project    			      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-90                               | Add suffix "ves" in job name.        |
|                                      |  				      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-94                               | Fix Major bugs, Vulnerabilities,     |
|                                      | Security issues as per Sonar job     |
|                                      | report                               |
+--------------------------------------+--------------------------------------+
| SMO-96                               | Introduce more test cases to improve |
|                                      | code coverage			      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-99                               | Write test cases for Standard Defined|
|                                      | Validator			      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-113                              | Add dependencies in tox file for CLM |
|                                      | job			              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+



Bug Corrections
^^^^^^^^^^^^^^^

**JIRA TICKETS:**

+--------------------------------------+--------------------------------------+
| **JIRA REFERENCE**                   | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-106 	                       | Fix failure of test case	      |
|                                      | 		      		      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-111 	                       | Unbale to run tox -e coverage        |
|                                      | 		      		      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| SMO-100 	                       | Sonar job is broken		      |
|                                      | 		      		      |
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


**LFN TICKETS:**

+--------------------------------------+--------------------------------------+
| **LFN REFERENCE**                    | **SLOGAN**                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| 		                       | 				      |
|     IT-24601                         | % of Coverage code is incorrect.     |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| 	                               |  				      |
|     IT-24305                         |  CLM job report is empty  	      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Workarounds
^^^^^^^^^^^
Working with the support team of the Linux Foundation to fix the problem.






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
#

import requests
import socket
import time

IPAddr = socket.gethostbyname(socket.gethostname())

influxdb_url = 'http://' + IPAddr + ':8086'
dmaap_url = 'http://' + IPAddr + ':5000/dmaapapi/v1'
collector_url = 'https://' + IPAddr + ':9999'

# Collector and InfluxDB connector flow test


def test_delete_pnfRegistration_event_from_influxdb():
    print("\nDeleting pnfRegistration event from influxdb")
    url = influxdb_url + "/query?q=DELETE FROM pnfRegistration where time=1641290592603290000&db=eventsdb"
    response = requests.get(url)
    assert "200" in str(response)
    print("Success")


def test_generate_pnfRegistration_event():
    print("\nGenerating pnfRegistration event")
    payload = {
        "event": {
            "commonEventHeader": {
                "domain": "pnfRegistration",
                "eventId": "NSHMRIACQ01M01123401_1234 BestInClass",
                "eventName": "pnfRegistration_EventType5G",
                "eventType": "EventType5G",
                "lastEpochMicrosec": 1641290592603261,
                "nfNamingCode": "1234",
                "nfVendorName": "VENDORA",
                "priority": "Low",
                "reportingEntityId": "",
                "reportingEntityName": "ORAN-DEV",
                "sequence": 0,
                "sourceId": "",
                "sourceName": "NSHMRIACQ01M01123401",
                "startEpochMicrosec": 1641290592603290,
                "timeZoneOffset": "+00:00",
                "version": "4.1",
                "vesEventListenerVersion": "7.2.1"
            },
            "pnfRegistrationFields": {
                "additionalFields": {
                    "betweenAttemptsTimeout": "2000",
                    "connectionTimeout": "20000",
                    "keepaliveDelay": "120",
                    "maxConnectionAttempts": "100",
                    "oamPort": "830",
                    "password": "netconf",
                    "protocol": "SSH",
                    "reconnectOnChangedSchema": "false",
                    "sleep-factor": "1.5",
                    "tcpOnly": "false",
                    "username": "netconf"
                    },
                "lastServiceDate": "2021-03-26",
                "macAddress": "02:42:f7:d4:62:ce",
                "manufactureDate": "2021-01-16",
                "modelNumber": "1234 BestInClass",
                "oamV4IpAddress": "10.10.10.11",
                "oamV6IpAddress": "0:0:0:0:0:ffff:a0a:011",
                "pnfRegistrationFieldsVersion": "2.1",
                "serialNumber": "VENDORA-1234-10.10.10.11-1234 BestInClass",
                "softwareVersion": "2.3.5",
                "unitFamily": "VENDORA-1234",
                "unitType": "1234",
                "vendorName": "VENDORA2"
                }
            }
        }

    response = requests.post(collector_url + "/eventListener/v7/events",
                             json=payload,
                             auth=('user', 'password'),
                             verify=False,
                             headers={"Content-Type": "application/json"})
    assert "202" in str(response)
    print("Success")


def test_delete_heartBeat_event_from_influxdb():
    print("\nDeleting heartbeat event from influxdb")
    url = influxdb_url + "/query?q=DELETE FROM heartbeat where time=1620196547427501000&db=eventsdb"
    response = requests.get(url)
    assert "200" in str(response)
    print("Success")


def test_generate_heartBeat_event():
    print("\nGenerating heartbeat event")
    payload = {
        "event": {
            "commonEventHeader": {
                "domain": "heartbeat",
                "eventId": "ORAN-DEV_2021-05-05T12:05:47.427501Z",
                "eventName": "heartbeat_O_RAN_COMPONENT",
                "eventType": "O_RAN_COMPONENT",
                "lastEpochMicrosec": 1620196547427501,
                "nfNamingCode": "SDN-Controller",
                "nfVendorName": "O-RAN-SC OAM",
                "priority": "Low",
                "reportingEntityId": "",
                "reportingEntityName": "ORAN-DEV",
                "sequence": 357,
                "sourceId": "",
                "sourceName": "ORAN-DEV",
                "startEpochMicrosec": 1620196547427501,
                "timeZoneOffset": "+00:00",
                "version": "4.1",
                "vesEventListenerVersion": "7.2.1"
            },
            "heartbeatFields": {
                "additionalFields": {
                    "eventTime": "2021-05-05T12:05:47.427501Z"
                    },
                "heartbeatFieldsVersion": "3.0",
                "heartbeatInterval": 20
            }
        }
    }

    response = requests.post(collector_url + "/eventListener/v7/events",
                             json=payload,
                             auth=('user', 'password'),
                             verify=False,
                             headers={"Content-Type": "application/json"})
    assert "202" in str(response)
    print("Success")


def test_delete_fault_event_from_influxdb():
    print("\nDeleting fault event from influxdb")
    url = influxdb_url + "/query?q=DELETE FROM fault where time=1620125339257359000&db=eventsdb"
    response = requests.get(url)
    assert "200" in str(response)
    print("Success")


def test_generate_fault_event():
    print("\nGenerating fault event")
    payload = {
        "event": {
            "commonEventHeader": {
                "domain": "fault",
                "eventId": "ORAN-DEV_northbound-interface_connectionLossNe",
                "eventName": "fault_ONAP_SDNR_Controller_Alarms_connectionLossNe",
                "eventType": "ONAP_SDNR_Controller_Alarms",
                "lastEpochMicrosec": 1620125339257359,
                "nfNamingCode": "SDNR",
                "nfVendorName": "ONAP",
                "priority": "High",
                "reportingEntityId": "",
                "reportingEntityName": "ORAN-DEV",
                "sequence": 0,
                "sourceId": "",
                "sourceName": "ORAN-DEV",
                "startEpochMicrosec": 1620125339257359,
                "timeZoneOffset": "+00:00",
                "version": "4.1",
                "vesEventListenerVersion": "7.2.1"
            },
            "faultFields": {
                "alarmAdditionalInformation": {
                    "equipType": "SDNR",
                    "eventTime": "2021-05-04T10:48:59.257359Z",
                    "model": "ONAP Controller for Radio",
                    "vendor": "ONAP"
                },
                "alarmCondition": "connectionLossNe",
                "alarmInterfaceA": "northbound-interface",
                "eventSeverity": "NORMAL",
                "eventSourceType": "ONAP_SDNR_Controller",
                "faultFieldsVersion": "4.0",
                "specificProblem": "connectionLossNe",
                "vfStatus": "Active"
            }
        }
      }

    response = requests.post(collector_url + "/eventListener/v7/events",
                             json=payload,
                             auth=('user', 'password'),
                             verify=False,
                             headers={"Content-Type": "application/json"})
    assert "202" in str(response)
    print("Success")


def test_delete_thresholdCrossingAlert_event_from_influxdb():
    print("\nDeleting thresholdCrossingAlert event from influxdb")
    url = influxdb_url + "/query?q=DELETE FROM thresholdCrossingAlert where time=1620125339257359000&db=eventsdb"
    response = requests.get(url)
    assert "200" in str(response)
    print("Success")


def test_generate_thresholdCrossingAlert_event():
    print("\nGenerating thresholdCrossingAlert event")
    payload = {
        "event": {
            "commonEventHeader": {
                "domain": "thresholdCrossingAlert",
                "eventId": "ORAN-DEV_northbound-interface_connectionLossNe",
                "eventName": "fault_ONAP_SDNR_Controller_Alarms_connectionLossNe",
                "eventType": "ONAP_SDNR_Controller_Alarms",
                "lastEpochMicrosec": 1620125339257359,
                "nfNamingCode": "SDNR",
                "nfVendorName": "ONAP",
                "priority": "High",
                "reportingEntityId": "",
                "reportingEntityName": "ORAN-DEV",
                "sequence": 0,
                "sourceId": "",
                "sourceName": "ORAN-DEV",
                "startEpochMicrosec": 1620125339257359,
                "timeZoneOffset": "+00:00",
                "version": "4.1",
                "vesEventListenerVersion": "7.2.1"
            },
            "thresholdCrossingAlertFields": {
                "additionalFields": {
                    "equipType": "1OSF",
                    "eventTime": "2021-05-03T10:49:04.968286Z",
                    "model": "",
                    "vendor": ""
                },
                "additionalParameters": [
                    {
                        "criticality": "MAJ",
                        "hashMap": {
                            "additionalProperties": "up-and-down"
                        },
                        "thresholdCrossed": "packetLoss"
                    }
                ],
                "alertAction": "CLEAR",
                "alertDescription": "TCA",
                "alertType": "INTERFACE-ANOMALY",
                "alertValue": "1OSF",
                "associatedAlertIdList": [
                    "loss-of-signal"
                ],
                "collectionTimestamp": "Mon, 03 May 2021 10:49:04 +0000",
                "dataCollector": "data-lake",
                "elementType": "1OSF",
                "eventSeverity": "NORMAL",
                "eventStartTimestamp": "Mon, 03 May 2021 10:45:00 +0000",
                "interfaceName": "",
                "networkService": "from-a-to-b",
                "possibleRootCause": "always-the-others",
                "thresholdCrossingFieldsVersion": "4.0"
            }
        }
      }

    response = requests.post(collector_url + "/eventListener/v7/events",
                             json=payload,
                             auth=('user', 'password'),
                             verify=False,
                             headers={"Content-Type": "application/json"})
    assert "202" in str(response)
    print("Success")


def test_delete_measurement_event_from_influxdb():
    print("\nDeleting measurement event from influxdb")
    url = influxdb_url + "/query?q=DELETE FROM \"measurement\" where time=1620125339257359000&db=eventsdb"
    response = requests.get(url)
    assert "200" in str(response)
    print("Success")


def test_generate_measurement_event():
    print("\nGenerating measurement event")
    payload = {
        "event": {
            "commonEventHeader": {
                "domain": "measurement",
                "eventId": "LKCYFL79Q01M01FYNG01_1620296100_PM15min",
                "eventName": "measurement_O_RAN_COMPONENT_PM15min",
                "eventType": "O_RAN_COMPONENT_PM15min",
                "internalHeaderFields": {
                    "intervalEndTime": "Thu, 06 May 2021 10:15:00 +0000",
                    "intervalStartTime": "Thu, 06 May 2021 10:00:00 +0000"
                },
                "lastEpochMicrosec": 1620125339257359,
                "priority": "Low",
                "reportingEntityId": "",
                "reportingEntityName": "ORAN-DEV",
                "sequence": 0,
                "sourceId": "",
                "sourceName": "LKCYFL79Q01M01FYNG01",
                "startEpochMicrosec": 1620125339257359,
                "version": "4.1",
                "vesEventListenerVersion": "7.2.1"
            },
            "measurementFields": {
                "additionalFields": {},
                "additionalMeasurements": [
                    {
                        "hashMap": {
                            "cses": "0",
                            "es": "0",
                            "ses": "1",
                            "unavailability": "0"
                        },
                        "name": "LP-MWPS-RADIO-1"
                    },
                    {
                        "hashMap": {
                            "cses": "0",
                            "es": "0",
                            "ses": "1",
                            "unavailability": "0"
                        },
                        "name": "LP-MWPS-RADIO-2"
                    }
                ],
                "additionalObjects": [],
                "codecUsageArray": [],
                "concurrentSessions": 2,
                "configuredEntities": 2,
                "cpuUsageArray": [],
                "diskUsageArray": [],
                "featureUsageArray": {
                    "https://www.itu.int/rec/T-REC-G.841": "true"
                },
                "filesystemUsageArray": [],
                "hugePagesArray": [],
                "ipmi": {},
                "latencyDistribution": [],
                "loadArray": [],
                "machineCheckExceptionArray": [],
                "meanRequestLatency": 1000,
                "measurementFieldsVersion": "4.0",
                "measurementInterval": 234,
                "memoryUsageArray": [],
                "nfcScalingMetric": 3,
                "nicPerformanceArray": [],
                "numberOfMediaPortsInUse": 234,
                "processStatsArray": [],
                "requestRate": 23,
                "networkSliceArray": [
                    {
                        "networkSliceIdentifier": "1020",
                        "DRB.UEThpUl.SNSSAI": 300,
                        "DRB.UEThpDl.SNSSAI": 400
                    },
                    {
                        "networkSliceIdentifier": "3838",
                        "DRB.UEThpUl.SNSSAI": 150,
                        "DRB.UEThpDl.SNSSAI": 250
                    },
                    {
                        "networkSliceIdentifier": "9872",
                        "DRB.UEThpUl.SNSSAI": 350,
                        "DRB.UEThpDl.SNSSAI": 450
                    }
                 ]
            }
        }
      }

    response = requests.post(collector_url + "/eventListener/v7/events",
                             json=payload,
                             auth=('user', 'password'),
                             verify=False,
                             headers={"Content-Type": "application/json"})
    assert "202" in str(response)
    print("Success")


def test_check_pnfRegistration_event():
    print("\nVerifying pnfRegistration event on influxdb")
    time.sleep(2)
    url = influxdb_url + "/query?q=SELECT COUNT(*) FROM pnfRegistration where time=1641290592603290000&db=eventsdb"
    response = requests.get(url)
    response_body = response.json()
    assert "pnfRegistration" in response_body['results'][0]['series'][0]['name']
    print("Success")


def test_check_measurement_event():
    print("\nVerifying measurement event on influxdb")
    time.sleep(2)
    url = influxdb_url + "/query?q=SELECT COUNT(*) FROM \"measurement\" where time=1620125339257359000&db=eventsdb"
    response = requests.get(url)
    response_body = response.json()
    assert "measurement" in response_body['results'][0]['series'][0]['name']
    print("Success")


def test_check_thresholdCrossingAlert_event():
    print("\nVerifying thresholdCrossingAlert event on influxdb")
    time.sleep(2)
    url = influxdb_url + "/query?q=SELECT COUNT(*) FROM thresholdCrossingAlert where time=1620125339257359000&db=eventsdb"
    response = requests.get(url)
    response_body = response.json()
    assert "thresholdCrossingAlert" in response_body['results'][0]['series'][0]['name']
    print("Success")


def test_check_fault_event():
    print("\nVerifying fault event on influxdb")
    time.sleep(2)
    url = influxdb_url + "/query?q=SELECT COUNT(*) FROM fault where time=1620125339257359000&db=eventsdb"
    response = requests.get(url)
    response_body = response.json()
    assert "fault" in response_body['results'][0]['series'][0]['name']
    print("Success")


def test_check_heartbeat_event():
    print("\nVerifying heartbeat event on influxdb")
    time.sleep(2)
    url = influxdb_url + "/query?q=SELECT COUNT(*) FROM heartbeat where time=1620196547427501000&db=eventsdb"
    response = requests.get(url)
    response_body = response.json()
    assert "heartbeat" in response_body['results'][0]['series'][0]['name']
    print("Success")

# DMAAP adapter APIs test


def test_dmaap_check_topics_api():
    print("\nVerifying " + dmaap_url + "/topics API")
    response = requests.get(dmaap_url + "/topics")
    response_body = response.json()
    assert "measurement" in response_body['topics']
    assert "fault" in response_body['topics']
    assert "heartbeat" in response_body['topics']
    assert "pnfregistration" in response_body['topics']
    assert "thresholdcrossingalert" in response_body['topics']
    print("Success")


def test_dmaap_check_topics_listall_api():
    print("\nVerifying " + dmaap_url + "/topics/listAll API")
    response = requests.get(dmaap_url + "/topics/listAll")
    response_body = response.json()
    topic_list = []
    for x in response_body['topics']:
        topic_list.append(x['topicName'])

    dict = {"topics": topic_list}
    assert "measurement" in dict['topics']
    assert "fault" in dict['topics']
    assert "heartbeat" in dict['topics']
    assert "pnfregistration" in dict['topics']
    assert "thresholdcrossingalert" in dict['topics']
    print("Success")


def test_dmaap_check_topic_measurement():
    print("\nVerifying " + dmaap_url + "/topics/measurement API")
    response = requests.get(dmaap_url + "/topics/measurement")
    response_body = response.json()
    assert "measurement" in response_body['name']
    print("Success")


def test_dmaap_check_topic_fault():
    print("\nVerifying " + dmaap_url + "/topics/fault API")
    response = requests.get(dmaap_url + "/topics/fault")
    response_body = response.json()
    assert "fault" in response_body['name']
    print("Success")


def test_dmaap_check_topic_heartbeat():
    print("\nVerifying " + dmaap_url + "/topics/heartbeat API")
    response = requests.get(dmaap_url + "/topics/heartbeat")
    response_body = response.json()
    assert "heartbeat" in response_body['name']
    print("Success")


def test_dmaap_check_topic_pnfregistration():
    print("\nVerifying " + dmaap_url + "/topics/pnfregistration API")
    response = requests.get(dmaap_url + "/topics/pnfregistration")
    response_body = response.json()
    assert "pnfregistration" in response_body['name']
    print("Success")


def test_dmaap_check_topic_thresholdcrossingalert():
    print("\nVerifying " + dmaap_url + "/topics/thresholdcrossingalert API")
    response = requests.get(dmaap_url + "/topics/thresholdcrossingalert")
    response_body = response.json()
    assert "thresholdcrossingalert" in response_body['name']
    print("Success")


def test_dmaap_check_events_api():
    print("\nVerifying /events API")
    response = requests.get(dmaap_url + "/events/fault/consumergroup1/consumerid1?limit=1&timeout=3")
    assert "200" in str(response)
    print("Success")

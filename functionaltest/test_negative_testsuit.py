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

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

dmaap_url = 'http://' + IPAddr + ':5000/dmaapapi/v1'
collector_url = 'https://' + IPAddr + ':9999'

# Collector and InfluxDB connector flow test


def test_invalid_domain():
    print("\nGenerating invalid event")
    payload = {
       "event": {
                "commonEventHeader": {
                    "domain": "pnfRegistratio",
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
    assert "400" in str(response)
    print("Success")


def test_dmaap_invalid_topic():
    print("\nChecking non-existent topic in /topics API")
    response = requests.get(dmaap_url + "/topics/testtopic")
    assert "404" in str(response)
    print("Success")


def test_dmaap_invalid_topic_in_event_api():
    print("\nChecking non-existent topic in /events API")
    response = requests.get(dmaap_url + "/events/testtopic/consumergroup1/consumerid1?limit=&timeout=5")
    assert "409" in str(response)
    print("Success")

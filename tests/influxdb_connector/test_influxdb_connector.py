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

from json import dumps
import json
import logging
import os
import pytest
import requests
import unittest
from influxdb_connector import *
import requests_mock
from pytest_mock import MockerFixture
from mock import patch

@pytest.fixture
def data_set():
    data_set = {
                "event": {
                    "commonEventHeader": {
                        "domain": "thresholdCrossingAlert",
                        "eventId": "__TCA",
                        "eventName": "thresholdCrossingAlert_O_RAN_COMPONENT_TCA_TCA",
                        "eventType": "O_RAN_COMPONENT_TCA",
                        "sequence": 0,
                        "priority": "High",
                        "reportingEntityId": "",
                        "reportingEntityName": "ORAN-DEV",
                        "sourceId": "",
                        "sourceName": "",
                        "startEpochMicrosec": 1639985336443218,
                        "lastEpochMicrosec": 1639985336443218,
                        "nfNamingCode": "1OSF",
                        "nfVendorName": "",
                        "timeZoneOffset": "+00:00",
                        "version": "4.1",
                        "vesEventListenerVersion": "7.2.1"
                    },
                    "thresholdCrossingAlertFields": {
                        "thresholdCrossingFieldsVersion": "4.0",
                        "additionalParameters": [{
                            "criticality": "MAJ",
                            "hashMap": { "additionalProperties": "up-and-down" },
                            "thresholdCrossed": "packetLoss"
                        }],
                        "alertAction": "SET",
                        "alertDescription": "TCA",
                        "alertType": "INTERFACE-ANOMALY",
                        "alertValue": "1OSF",
                        "associatedAlertIdList": ["loss-of-signal"],
                        "collectionTimestamp": "Mon, 20 Dec 2021 07:28:56 +0000",
                        "dataCollector": "data-lake",
                        "elementType": "1OSF",
                        "eventSeverity": "WARNING",
                        "eventStartTimestamp": "Mon, 20 Dec 2021 07:15:00 +0000",
                        "interfaceName": "",
                        "networkService": "from-a-to-b",
                        "possibleRootCause": "always-the-others",
                        "additionalFields": {
                            "eventTime": "2021-12-20T07:28:56.443218Z",
                            "equipType": "1OSF",
                            "vendor": "",
                            "model": ""
                        }
                    }
                }
            }
    return data_set

# <Response [204]>
def test_send_event_to_influxdb_successfully(data_set):
    """
    Simply test event should store in influxdb successfully.
    """
    with requests_mock.Mocker() as rm:
        rm.post('http://localhost:8086/write?db=eventsdb', json=data_set, status_code=204)
        response = requests.post(
        'http://localhost:8086/write?db=eventsdb', data=data_set
    )
        assert response.status_code == 204

# <Response [400]>
def test_send_event_to_influxdb_failed(data_set):
    """
    Bad Request.
    """
    with requests_mock.Mocker() as rm:
        rm.post('http://localhost:8086/write?db=eventsdb', json=data_set, status_code=400)
        response = requests.post(
        'http://localhost:8086/write?db=eventsdb', data=data_set
    )
        assert response.status_code == 400

def test_process_time():
    assert process_time(int(1639983600000)) == '1639983600000000000'


def test_process_special_char():
    assert process_special_char("7.2.1") == '7.2.1'

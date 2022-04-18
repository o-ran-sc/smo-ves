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

import json
import pytest
from prepare_response import PrepareResponse
from pytest_mock import MockerFixture


@pytest.fixture
def response_object():
    return PrepareResponse()


def test_setResponseCode(response_object):
    response_object.setResponseCode("200")
    assert response_object.getResponseCode() == '200'

def test_setResponseMsg(response_object, data_set):
    response_object.setResponseMsg(data_set)
    assert json.loads(response_object.getResponseMsg()) == data_set


def test_getResponseCode(response_object):
    response_object.setResponseCode("200")
    assert response_object. getResponseCode() == '200'

    
def test_getResponseMsg(response_object, data_set):
    response_object.setResponseMsg(data_set)
    assert json.loads(response_object.getResponseMsg()) == data_set
    
    
@pytest.fixture
def data_set():
    data_set = {
               "event": {
                  "commonEventHeader": {
                     "domain": "measurement",
                     "eventId": "5",
                     "eventName": "",
                     "eventType": "platform",
                     "lastEpochMicrosec": 0,
                     "priority": "Normal",
                     "reportingEntityId": "localhost",
                     "reportingEntityName": "localhost",
                     "sequence": 0,
                     "sourceName": "bf9006ed-a735-064a-871c-4b4debe57935",
                     "startEpochMicrosec": 1643798824.813,
                     "version": "4.0",
                     "vesEventListenerVersion": "7.2.1",
                     "sourceId": "bf9006ed-a735-064a-871c-4b4debe57935"
                  },
                  "measurementFields": {
                     "measurementFieldsVersion": "4.0",
                     "measurementInterval": 10,
                     "loadArray": [
                        {
                           "midTerm": 4.12,
                           "shortTerm": 5.14,
                           "longTerm": 2.22
                        }
                     ],
                     "memoryUsageArray": [
                        {
                           "vmIdentifier": "bf9006ed-a735-064a-871c-4b4debe57935",
                           "memoryFree": 489902080,
                           "memoryUsed": 5010788,
                           "memoryBuffered": 249216,
                           "memoryCached": 2080804,
                           "memorySlabRecl": 175884,
                           "memorySlabUnrecl": 153208
                        }
                     ],
                     "cpuUsageArray": [
                        {
                           "cpuIdentifier": "0",
                           "cpuIdle": 92.6977687626775,
                           "percentUsage": 0,
                           "cpuUsageUser": 6.08519269776876,
                           "cpuWait": 0.304259634888438,
                           "cpuUsageInterrupt": 0,
                           "cpuUsageNice": 0,
                           "cpuUsageSoftIrq": 0.202839756592292,
                           "cpuUsageSteal": 0,
                           "cpuUsageSystem": 0.709939148073022
                        },
                        {
                           "cpuIdentifier": "3",
                           "cpuIdle": 90.8722109533469,
                           "percentUsage": 0,
                           "cpuUsageUser": 6.08519269776876,
                           "cpuWait": 2.23123732251521,
                           "cpuUsageInterrupt": 0,
                           "cpuUsageNice": 0,
                           "cpuUsageSoftIrq": 0.202839756592292,
                           "cpuUsageSteal": 0,
                           "cpuUsageSystem": 0.608519269776876
                        }
                     ]
                  }
               }
            }
    return json.dumps(data_set)
    

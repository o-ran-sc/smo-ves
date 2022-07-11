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
from _pytest.mark import param
from flask import request
import flask
from future.backports.urllib import response
from mock import MagicMock
from pathlib import Path
import pytest
import requests
from unittest import mock
from unittest.mock import patch
from consumer import EventConsumer, TopicConsumer
import dmaap_adapter
from prepare_response import PrepareResponse

@pytest.fixture
def response_object():
    return PrepareResponse()

@pytest.fixture
def prepareResponse(response_object, data_set):
    response_object.setResponseCode("200")
    response_object.setResponseMsg(data_set)
    return response_object

@mock.patch('flask.Flask.response_class')
@mock.patch('dmaap_adapter.PrepareResponse')
@mock.patch('dmaap_adapter.TopicConsumer')
def test_get_all_topics(mock_consumer, mock_response, mock_app, prepareResponse, data_set):
    mock_app.return_value = prepareResponse
    res = dmaap_adapter.get_all_topics()
    mock_consumer.getTopics(mock_response)
    mock_consumer.getTopics.assert_called_with(mock_response)
    assert res.responseCode == prepareResponse.getResponseCode()

@mock.patch('flask.Flask.response_class')
@mock.patch('dmaap_adapter.PrepareResponse')
@mock.patch('dmaap_adapter.TopicConsumer')
def test_listall_topics(mock_consumer, mock_response, mock_app, prepareResponse, data_set):
    mock_app.return_value = prepareResponse
    res = dmaap_adapter.listall_topics()
    mock_consumer.listAllTopics(mock_response)
    mock_consumer.listAllTopics.assert_called_with(mock_response)
    assert res.responseCode == prepareResponse.getResponseCode()

@pytest.mark.skip
@mock.patch('flask.request')
@mock.patch('flask.Flask.response_class')
@mock.patch('dmaap_adapter.PrepareResponse')
@mock.patch('dmaap_adapter.TopicConsumer')
def test_topic_details(mock_consumer, mock_response, mock_app, mock_req, prepareResponse, data_set, topic):
    mock_app.return_value = prepareResponse
    res = dmaap_adapter.topic_details(topic)
    mock_consumer.getTopicDetails(mock_response, topic)
    mock_consumer.getTopicDetails.assert_called_with(mock_response, topic)
    assert res.responseCode == prepareResponse.getResponseCode()

@pytest.mark.skip
@mock.patch('flask.Flask.response_class')
@mock.patch('dmaap_adapter.PrepareResponse')
@mock.patch('dmaap_adapter.EventConsumer')
def test_get_events(mock_consumer, mock_response, mock_app, prepareResponse, data_set, topic):
    mock_app.return_value = prepareResponse
    res = dmaap_adapter.get_events(topic, "consumergroup", "consumerid")
    mock_consumer.consumeEvents(mock_response, topic, "consumergroup", "consumerid", 10, 15)
    mock_consumer.consumeEvents.assert_called_with(mock_response, topic, "consumergroup", "consumerid", 10, 15)
    assert res.responseCode == prepareResponse.getResponseCode()

@pytest.fixture
def topic():
    topic_name = "measurement"
    return topic_name

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
                     ],
                     "nicPerformanceArray": [
                        {
                           "valuesAreSuspect": "true",
                           "nicIdentifier": "vethad656aa",
                           "receivedTotalPacketsAccumulated": 6.60006078986562,
                           "transmittedTotalPacketsAccumulated": 15.1001390798441,
                           "receivedOctetsAccumulated": 2453.82247547105,
                           "transmittedOctetsAccumulated": 7411.46788438591,
                           "receivedErrorPacketsAccumulated": 0,
                           "transmittedErrorPacketsAccumulated": 0,
                           "receivedDiscardedPacketsAccumulated": 0,
                           "transmittedDiscardedPacketsAccumulated": 0
                        }
                     ],
                     "diskUsageArray": [
                        {
                           "diskIdentifier": "loop12",
                           "diskOctetsReadLast": 0,
                           "diskOctetsWriteLast": 0,
                           "diskOpsReadLast": 0,
                           "diskOpsWriteLast": 0,
                           "diskIoTimeLast": 0,
                           "diskMergedReadLast": 0,
                           "diskMergedWriteLast": 0,
                           "diskTimeReadLast": 0,
                           "diskTimeWriteLast": 0
                        },
                        {
                           "diskIdentifier": "loop13",
                           "diskOctetsReadLast": 0,
                           "diskOctetsWriteLast": 0,
                           "diskOpsReadLast": 0,
                           "diskOpsWriteLast": 0,
                           "diskIoTimeLast": 0,
                           "diskMergedReadLast": 0,
                           "diskMergedWriteLast": 0,
                           "diskTimeReadLast": 0,
                           "diskTimeWriteLast": 0
                        }
                     ]
                  }
               }
            }
    return data_set

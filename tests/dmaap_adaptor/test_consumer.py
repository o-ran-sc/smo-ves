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


import pytest
from unittest import mock
from unittest.mock import patch
from pytest_mock import MockerFixture
from prepare_response import PrepareResponse
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient
from consumer import EventConsumer, TopicConsumer
import logging

@pytest.fixture
def prepareResponse():
    return PrepareResponse()

@pytest.fixture
def topic():
    topic_name = "test1"
    return topic_name

@pytest.fixture
def topic_list():
    topic_list=ListTopics()
    return topic_list

@pytest.fixture
def resCode():
    responseCode=200
    return responseCode

@mock.patch('confluent_kafka.Consumer')
def test_consumeEvents(mock_consumer,prepareResponse,topic,resCode):
    consumergroup="test"
    consumerid="test1"
    limit=10
    timeout=1
    mock_consumer.__name__ = 'subscribe'
    mock_consumer.__name__ = 'poll'
    mock_consumer.poll.return_value=None
    EventConsumer.consumeEvents(EventConsumer, prepareResponse, topic, consumergroup, consumerid,limit, timeout)
    resMsg='[]'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()

def test_getTopics(mocker,prepareResponse,topic_list,resCode):
    mocker.patch('confluent_kafka.admin.AdminClient.list_topics',
    return_value=topic_list)
    TopicConsumer.getTopics(TopicConsumer, prepareResponse)
    resMsg='{"topics": ["test1", "test2"]}'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()

def test_listAllTopics(mocker,prepareResponse,topic_list,resCode):
    mocker.patch('confluent_kafka.admin.AdminClient.list_topics',
    return_value=topic_list)
    TopicConsumer.listAllTopics(TopicConsumer, prepareResponse)
    resMsg='{"topics": [{"topicName": "test1", "owner": "", "txenabled": false}, {"topicName": "test2", "owner": "", "txenabled": false}]}'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()

def test_getTopicDetails(mocker,prepareResponse,topic,topic_list,resCode):
    mocker.patch('confluent_kafka.admin.AdminClient.list_topics',
    return_value=topic_list)
    TopicConsumer.getTopicDetails(TopicConsumer, prepareResponse,topic)
    resMsg='{"name": "test1", "owner": "", "description": "", "readerAcl": {"enabled": true, "users": []}, "writerAcl": {"enabled": true, "users": []}}'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()

class ListTopics:
    topics={"test1":"value1", "test2":"value2"}

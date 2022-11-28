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

import os
import argparse
import abc
import pytest
from unittest import mock
from unittest.mock import patch
from pytest_mock import MockerFixture
from prepare_response import PrepareResponse
from confluent_kafka import Consumer, KafkaError
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
    topic_list = ListTopics()
    return topic_list


@pytest.fixture
def empty_topic_list():
    empty_topic_list = EmptyListTopics()
    return empty_topic_list


@pytest.fixture
def resCode():
    responseCode = 200
    return responseCode


def get_path():
    project_path = os.getcwd()
    return project_path


def get_config_path():
    project_path = get_path()
    config_path = os.path.join(project_path, "tests/dmaap_adaptor/test_config.conf")
    return config_path


@mock.patch("confluent_kafka.Consumer")
def test_consumeEvents(mock_consumer, prepareResponse, topic, resCode):
    consumergroup = "test"
    consumerid = "test1"
    limit = 10
    timeout = 1
    mock_consumer.__name__ = "subscribe"
    mock_consumer.__name__ = "poll"
    mock_consumer.poll.return_value = None
    EventConsumer.consumeEvents(
        EventConsumer, prepareResponse, topic, consumergroup, consumerid, limit, timeout
    )
    resMsg = "[]"
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test __init__()function of TpoicConsumer
@mock.patch("app_config.AppConfig.setLogger")
@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(config=get_config_path(), section="default"),
)
def test_init_consumer(parser, mock_setLogger):
    TopicConsumer.__init__(TopicConsumer)
    mock_setLogger.assert_called_with("dmaap.log", "error")


# test __init__() function of EventConsumer
@mock.patch("app_config.AppConfig.setLogger")
@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(config=get_config_path(), section="default"),
)
def test_init_event(parser, mock_setLogger):
    EventConsumer.__init__(EventConsumer)
    mock_setLogger.assert_called_with("dmaap.log", "error")


# test consumeEvents for break
@mock.patch("confluent_kafka.Consumer")
def test_consumeEvents_break(mock_consumer, prepareResponse, topic, resCode):
    consumergroup = "test"
    consumerid = "test1"
    limit = 0
    timeout = 1
    mock_consumer.__name__ = "subscribe"
    mock_consumer.__name__ = "poll"
    mock_consumer.poll.return_value = None
    resMsg = "[]"
    EventConsumer.consumeEvents(
        EventConsumer, prepareResponse, topic, consumergroup, consumerid, limit, timeout
    )
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test consumeEvents for Exception
@mock.patch("confluent_kafka.Consumer")
def test_consumeEvents_Exceptions(mock_consumer, prepareResponse, topic):
    consumergroup = "test"
    consumerid = "test1"
    limit = abc
    timeout = 1
    mock_consumer.__name__ = "subscribe"
    mock_consumer.__name__ = "poll"
    mock_consumer.poll.return_value = None
    resMsg = '"Failed to return the events"'
    EventConsumer.consumeEvents(
        EventConsumer, prepareResponse, topic, consumergroup, consumerid, limit, timeout
    )
    assert 500 == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


def test_getTopics(mocker, prepareResponse, topic_list, resCode):
    mocker.patch(
        "confluent_kafka.admin.AdminClient.list_topics", return_value=topic_list
    )
    TopicConsumer.getTopics(TopicConsumer, prepareResponse)
    resMsg = '{"topics": ["test1", "test2"]}'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test getTopics Exception
def test_getTopics_Exceptions(mocker, prepareResponse):
    mocker.patch("confluent_kafka.admin.AdminClient.list_topics", return_value="")
    TopicConsumer.getTopics(TopicConsumer, prepareResponse)
    resMsg = '"Failed to return the topics"'
    assert 500 == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test ListALLTopics() function
def test_listAllTopics(mocker, prepareResponse, topic_list, resCode):
    mocker.patch(
        "confluent_kafka.admin.AdminClient.list_topics", return_value=topic_list
    )
    TopicConsumer.listAllTopics(TopicConsumer, prepareResponse)
    resMsg = '{"topics": [{"topicName": "test1", "owner": "", "txenabled": false}, {"topicName": "test2", "owner": "", "txenabled": false}]}'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test listAllTopics Exceptions
def test_listAllTopics_Exceptions(mocker, prepareResponse):
    mocker.patch("confluent_kafka.admin.AdminClient.list_topics", return_value="")
    TopicConsumer.listAllTopics(TopicConsumer, prepareResponse)
    resMsg = '"Failed to return the topics"'
    assert 500 == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test getTopicDetails() function
def test_getTopicDetails(mocker, prepareResponse, topic, topic_list, resCode):
    mocker.patch(
        "confluent_kafka.admin.AdminClient.list_topics", return_value=topic_list
    )
    TopicConsumer.getTopicDetails(TopicConsumer, prepareResponse, topic)
    resMsg = '{"name": "test1", "owner": "", "description": "", "readerAcl": {"enabled": true, "users": []}, "writerAcl": {"enabled": true, "users": []}}'
    assert resCode == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test getTopicDetails Exceptions
def test_getTopicDetails_Exceptions(mocker, prepareResponse, topic):
    mocker.patch("confluent_kafka.admin.AdminClient.list_topics", return_value="")
    TopicConsumer.getTopicDetails(TopicConsumer, prepareResponse, topic)
    resMsg = '"Failed to return the topics"'
    assert 500 == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


# test getTopicDetails Topic exists
def test_getTopicDetails_Topic_exists(
    mocker, prepareResponse, topic, empty_topic_list, resCode
):
    mocker.patch(
        "confluent_kafka.admin.AdminClient.list_topics", return_value=empty_topic_list
    )
    TopicConsumer.getTopicDetails(TopicConsumer, prepareResponse, topic)
    resMsg = '"Topic [test1] not found"'
    assert 404 == prepareResponse.getResponseCode()
    assert resMsg == prepareResponse.getResponseMsg()


class ListTopics:
    topics = {"test1": "value1", "test2": "value2"}


class EmptyListTopics:
    topics = {}

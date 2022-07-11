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
import pytest
import unittest
import monitor
import argparse
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from unittest import mock
from unittest.mock import patch
import logging
from pytest_mock import MockerFixture
from gevent import socket
from json import dumps
from gevent import pywsgi
import gevent
import json
import jsonschema
from kafka import KafkaProducer


def get_path():
    project_path = os.getcwd()
    project_path = project_path[:project_path.rfind('/')]
    return project_path

def get_config_path():
    project_path=get_path()
    config_path = os.path.join(
        project_path,"ves/tests/collector/test_collector.conf")
    return config_path

def get_schema_path():
    project_path=get_path()
    schema_path = os.path.join(
    project_path,"ves/collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-2.json")
    return schema_path

@pytest.fixture
def body():
    body={"event": {"commonEventHeader": {"domain": "measurement","eventId": "11","eventName": "","eventType": "platform","lastEpochMicrosec": 0,"priority": "Normal","reportingEntityId": "localhost","reportingEntityName": "localhost","sequence": 0,"sourceId": "776f3123-30a5-f947-bdf5-099ec3a7577a","sourceName": "776f3123-30a5-f947-bdf5-099ec3a7577a","startEpochMicrosec": 1642961518.919,"version": "4.0","vesEventListenerVersion": "7.2.1"}}}
    body=json.dumps(body)
    return body

@pytest.fixture
def start_response():
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_response=pywsgi.WSGIHandler(sock,"","")
    return start_response

@pytest.fixture
def schema():
    schema_path = get_schema_path()
    schema=json.load(open(schema_path, 'r'))
    return schema

@pytest.fixture
def data_set():
    data_set={"event": {"commonEventHeader": {"domain": "topic" }}}
    return data_set

@pytest.fixture
def topic_name():
    topic_name="topic"
    return topic_name

#@pytest.mark.skip
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    with mock.patch.object(logger,'debug') as mock_debug:
        monitor.listener(environ,mock_start_response,schema)

@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_config_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main(server,parser,body):
    argv=None
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.ERROR)
    with mock.patch.object(logger,'error') as mock_error:
        monitor.main(argv=None)
        #server.assert_called_once_with()
        mock_error.assert_called_once_with('Main loop exited unexpectedly!')

#@pytest.mark.skip
@mock.patch('monitor.kafka_server')
def test_save_event_in_kafka(mocker,data_set,topic_name):
    data_set_string=json.dumps(data_set)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.INFO)
    mocker.patch('monitor.produce_events_in_kafka')
    with mock.patch.object(logger,'info') as mock_info:
        monitor.save_event_in_kafka(data_set_string)
        mock_info.assert_called_once_with('Got an event request for topic domain')
        #monitor.produce_events_in_kafka.assert_called_once_with(data_set,topic_name)


@mock.patch('monitor.KafkaProducer')
@mock.patch('monitor.producer')
def test_produce_events_in_kafka(mock_pro,mock_producer,data_set,topic_name):
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    with mock.patch.object(logger,'debug') as mock_debug:
        monitor.produce_events_in_kafka(data_set,topic_name)
        mock_pro.send.assert_called_with(topic_name,value=data_set)
        mock_debug.assert_called_once_with('Event has been successfully posted into kafka bus')


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

import shutil
import os
import pytest
import unittest
import monitor
import argparse
import configparser
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock
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
    return project_path

def get_config_path():
    project_path=get_path()
    config_path = os.path.join(
        project_path,"tests/collector/test_collector.conf")
    return config_path

def get_wrong_config_path():
    project_path=get_path()
    config_path = os.path.join(
        project_path,"tests/collector/wrong_config.conf")
    return config_path

def get_wrong_config_port_path():
    project_path=get_path()
    config_path = os.path.join(
        project_path,"tests/collector/port_config.conf")
    return config_path

def get_schema_path():
    project_path=get_path()
    schema_path = os.path.join(
    project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-2.json")
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


def test_init():
   obj=monitor.JSONObject({})
   assert obj.__dict__=={}


#@pytest.mark.skip
@patch('monitor.logger',logging.getLogger('monitor'))
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
        result=list(monitor.listener(environ,mock_start_response,schema))
        assert result==[b'']


#test for listener Exception
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_exp(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2","PATH_INFO": '/eventListener/v5/events'}
    body={}
    mock_input.read.return_value=json.dumps(body)
    mock_start_response= mock.Mock(start_response)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-1.json")}
    try:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))

    except TypeError:
        assert result == None
    except Exception:
        pytest.fail('unexcepted error')


#test b64decode credentials in listener()
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_b64decode(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "None None", "CONTENT_LENGTH": "2","PATH_INFO": '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.WARN)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-1.json")}
    with mock.patch.object(logger,'warn') as mock_warn:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))
        mock_monitor.assert_called_with(body)


#test listener pending command list
@patch('monitor.vel_username','user')
@patch('monitor.vel_password','password')
@patch('monitor.logger',logging.getLogger('monitor'))
@patch('monitor.pending_command_list',[1,2,3])
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_command_list(mock_monitor,mock_input,body,start_response,schema,topic_name):
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2", 'PATH_INFO': '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-2.json")}
    with mock.patch.object(logger,'debug') as mock_debug:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))
        assert [b'[1, 2, 3]'] ==result


#test listener if pending_command list is none
@patch('monitor.vel_username','user')
@patch('monitor.vel_password','password')
@patch('monitor.logger',logging.getLogger('monitor'))
@patch('monitor.pending_command_list',None)
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_command_list_none(mock_monitor,mock_input,body,start_response,schema,topic_name):
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2", 'PATH_INFO': '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-1.json")}
    with mock.patch.object(logger,'debug') as mock_debug:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))
        assert [b'']==result  


#test jsonschema error
@patch('monitor.vel_username','user')
@patch('monitor.vel_password','password')
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_schema_none(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2","PATH_INFO": '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    project_path=os.getcwd()
    dict_schema =os.path.join(project_path,"tests/collector/schema.json")
    os._exit = mock.MagicMock()
    list(monitor.listener(environ, mock_start_response, dict_schema))
    assert os._exit.called   



#test jsonschema validation exception
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_jsonschema_validation(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={"event": {"commonEventHeader": {"domain": 6,"eventId": "11","eventName": "","eventType": "platform","lastEpochMicrosec": 0,"priority": "Normal","reportingEntityId": "localhost","reportingEntityName": "localhost","sequence": 0,"sourceId": "776f3123-30a5-f947-bdf5-099ec3a7577a","sourceName": "776f3123-30a5-f947-bdf5-099ec3a7577a","startEpochMicrosec": 1642961518.919,"version": "4.0","vesEventListenerVersion": "7.2.1"}}}
    body=json.dumps(body)
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,schema))
    assert [b'']==result



#test for listener Exception
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_exp(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2","PATH_INFO": '/eventListener/v5/events'}
    body={}
    mock_input.read.return_value=json.dumps(body)
    mock_start_response= mock.Mock(start_response)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-1.json")}
    try:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))

    except TypeError:
        assert result == None
    except Exception:
        pytest.fail('unexcepted error')


#test b64decode credentials in listener()
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_b64decode(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "None None", "CONTENT_LENGTH": "2","PATH_INFO": '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.WARN)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-1.json")}
    with mock.patch.object(logger,'warn') as mock_warn:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))
        mock_monitor.assert_called_with(body)


#test listener pending command list
@patch('monitor.vel_username','user')
@patch('monitor.vel_password','password')
@patch('monitor.logger',logging.getLogger('monitor'))
@patch('monitor.pending_command_list',[1,2,3])
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_command_list(mock_monitor,mock_input,body,start_response,schema,topic_name):
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2", 'PATH_INFO': '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-2.json")}
    with mock.patch.object(logger,'debug') as mock_debug:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))
        assert [b'[1, 2, 3]'] ==result


#test listener if pending_command list is none
@patch('monitor.vel_username','user')
@patch('monitor.vel_password','password')
@patch('monitor.logger',logging.getLogger('monitor'))
@patch('monitor.pending_command_list',None)
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_command_list_none(mock_monitor,mock_input,body,start_response,schema,topic_name):
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2", 'PATH_INFO': '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    project_path = os.getcwd()
    dict_schema = {"v5": os.path.join(project_path,"collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-1.json")}
    with mock.patch.object(logger,'debug') as mock_debug:
        result = list(monitor.listener(environ, mock_start_response, dict_schema))
        assert [b'']==result  


#test jsonschema error
@patch('monitor.vel_username','user')
@patch('monitor.vel_password','password')
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_schema_none(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2","PATH_INFO": '/eventListener/v5/events'}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    project_path=os.getcwd()
    dict_schema =os.path.join(project_path,"tests/collector/schema.json")
    os._exit = mock.MagicMock()
    list(monitor.listener(environ, mock_start_response, dict_schema))
    assert os._exit.called   



#test jsonschema validation exception
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_jsonschema_validation(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={"event": {"commonEventHeader": {"domain": 6,"eventId": "11","eventName": "","eventType": "platform","lastEpochMicrosec": 0,"priority": "Normal","reportingEntityId": "localhost","reportingEntityName": "localhost","sequence": 0,"sourceId": "776f3123-30a5-f947-bdf5-099ec3a7577a","sourceName": "776f3123-30a5-f947-bdf5-099ec3a7577a","startEpochMicrosec": 1642961518.919,"version": "4.0","vesEventListenerVersion": "7.2.1"}}}
    body=json.dumps(body)
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,schema))
    assert [b'']==result



#test if schema is none
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_schma_is_empty(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result



#test listener() Exception event is invalid for unexpected reason
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_Event_Invalid(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result


#test listener() standardDefineFields
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('monitor.stnd_define_event_validation')
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_stdDefined_field(mock_monitor,mock_input,mock_std,body,start_response,schema,topic_name):
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={"event":{"stndDefinedFields":{"schemaReference":"https://forge.3gpp.org"}}}
    mock_input.read.return_value=json.dumps(body)
    mock_start_response= mock.Mock(start_response)
    project_path = os.getcwd()
    dict_schema =os.path.join(project_path,"tests/collector/stdDefine.json")
    schema=json.load(open(dict_schema,'r'))
    result = list(monitor.listener(environ, mock_start_response,schema))
    mock_std.assert_called_once_with(None,body)


#test listener standardDefineFields schema_ref not found
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_stdDefine_schema_ref(mock_monitor,mock_input,body,start_response,schema,topic_name):
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={"event":{"stndDefinedFields":{"schemaReference":""}}}
    mock_input.read.return_value=json.dumps(body)
    mock_start_response= mock.Mock(start_response)
    project_path = os.getcwd()
    dict_schema =os.path.join(project_path,"tests/collector/stdDefine.json")
    schema=json.load(open(dict_schema,'r'))
    result = list(monitor.listener(environ, mock_start_response,schema))
    assert [b'']==result





#test if schema is none
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_schma_is_empty(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result



#test listener() Exception event is invalid for unexpected reason
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_Event_Invalid(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result





#test if schema is none
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_schma_is_empty(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result



#test listener() Exception event is invalid for unexpected reason
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_Event_Invalid(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result




#test if schema is none
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_schma_is_empty(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result



#test listener() Exception event is invalid for unexpected reason
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_Event_Invalid(mock_monitor,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.listener(environ,mock_start_response,None))
    assert []==result



#check main() function
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_config_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
@mock.patch('monitor.logger', logging.getLogger('monitor'))
def test_main(server,parser,body):
    argv=None
    result=monitor.main(argv=None)
    assert 0==result
    


#test main() function argv is None
@patch('monitor.logger')
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=2, api_version='7',config=get_config_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main_argv(server,parser,logger,body):
    argv=''
    logger.return_value=logging.getLogger('monitor')
    try:
        result=monitor.main(argv)
    except TypeError:
        assert result == None
    except Exception:
        pytest.fail('unexcepted error')



#test platform.system in main
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_config_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main_platform(server,parser,body):
    argv=None
    sys = mock.MagicMock()
    try:
        with patch('platform.system', MagicMock(return_value='Windows')):
            res=monitor.main(argv)
    except RuntimeError:
        assert res == None
    except Exception:
        pytest.fail('Exiting because of exception')


#test vel_port in main
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_wrong_config_port_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main_vel_port(server,parser,body):
    argv=''
    res=monitor.main(argv)
    assert res == 2



# test vel_path in main
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_wrong_config_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main_path(server,parser,body):
    argv=None
    try:
        result = monitor.main(argv)
    except RuntimeError:
        assert result == None
    except Exception:
        pytest.fail('fail beacuase of exception')



@pytest.fixture
def vel_schema_path():
    config = configparser.ConfigParser()
    config_file=get_config_path()
    config.read(config_file)
    ref = config.get('default', 'schema_file')
    return ref


# check main() vel_schema, if it exists
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_config_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main_vel_schema_path(server,parser,vel_schema_path):
    argv=None
    with mock.patch('os.path.exists') as m:
        m.return_value=vel_schema_path
        result=monitor.main(argv)
        assert 0==result



#test unhandle exception
@patch('monitor.DEBUG',True)
@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(verbose=None, api_version='7',config=get_wrong_config_port_path(),section='default'))
@mock.patch('gevent.pywsgi.WSGIServer.serve_forever')
def test_main_unhandle_exception(server,parser,body):
    argv=None
    result=None
    try:
        result = monitor.main(argv)
    except RuntimeError:
        assert result == None
    except Exception:
        pytest.fail('Exiting because of exception')



#check test_listener() function
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_listener(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.test_listener(environ,mock_start_response,schema))
    assert ['']==result



#check test_listener() GET method
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_listener_get_method(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "GET","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    response= ['{"event": {"commonEventHeader": {"domain": "measurement", "eventId": "11", "eventName": "", "eventType": "platform", "lastEpochMicrosec": 0, "priority": "Normal", "reportingEntityId": "localhost", "reportingEntityName": "localhost", "sequence": 0, "sourceId": "776f3123-30a5-f947-bdf5-099ec3a7577a", "sourceName": "776f3123-30a5-f947-bdf5-099ec3a7577a", "startEpochMicrosec": 1642961518.919, "version": "4.0", "vesEventListenerVersion": "7.2.1"}}}']
    result=list(monitor.test_listener(environ,mock_start_response,schema))
    assert response==result


#test test_listener() jsonschema error
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_listener_schema_error(mocker,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    project_path=os.getcwd()
    schema_path =os.path.join(project_path,"tests/collector/schema.json")
    schema=json.load(open(schema_path, 'r'))
    result=list(monitor.test_listener(environ, mock_start_response,schema))
    assert ['']==result


#test test_listener() jsonschema validation error
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_listener_schema_validation_error(mocker,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={"event": {"commonEventHeader": {"domain": 6,"eventId": "11","eventName": "","eventType": "platform","lastEpochMicrosec": 0,"priority": "Normal","reportingEntityId": "localhost","reportingEntityName": "localhost","sequence": 0,"sourceId": "776f3123-30a5-f947-bdf5-099ec3a7577a","sourceName": "776f3123-30a5-f947-bdf5-099ec3a7577a","startEpochMicrosec": 1642961518.919,"version": "4.0","vesEventListenerVersion": "7.2.1"}}}
    body=json.dumps(body)
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.test_listener(environ, mock_start_response,schema))
    assert ['']==result



@pytest.fixture
def schema_wrong():
    schema_path ="/home/ves-dev/ves/tests/collector/schema.json"
    schema=json.load(open(schema_path, 'r'))
    return schema


#test test_listener() exception TestControl input not valid
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_listener_exception(mocker,mock_input,body,start_response,schema_wrong):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.test_listener(environ, mock_start_response,schema_wrong))
    assert ['']==result



#check test_listener() Missing schema 
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_listener_Missing_schema(mocker,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.test_listener(environ, mock_start_response,None))
    assert ['']==result


#check test_listener() Invalid Input
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_TestControl_Listener_Input_invalid(mocker,mock_input,body,start_response):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "POST","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    body={}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result=list(monitor.test_listener(environ, mock_start_response,None))
    assert ['']==result


#test listener() get method
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('gevent.pywsgi.Input',autospec=True)
@mock.patch('monitor.save_event_in_kafka')
def test_listener_get_method(mock_monitor,mock_input,body,start_response,schema):
    mock_input.__name__ = 'read'
    environ={"REQUEST_METHOD": "GET","wsgi.input": mock_input,"CONTENT_TYPE": "application/json","HTTP_AUTHORIZATION": "Basic dXNlcjpwYXNzd29yZA==", "CONTENT_LENGTH": "2"}
    mock_input.read.return_value=body
    mock_start_response= mock.Mock(start_response)
    result = list(monitor.listener(environ, mock_start_response, schema))
    assert [b'POST  /eventListener/v7'] == result



@pytest.fixture
def vel_schema_path():
    path=os.getcwd()
    vel_schema_path=os.path.join(path,"collector/evel-test-collector/docs/schema")
    return vel_schema_path


@pytest.fixture
def schema_ref():
    config = configparser.ConfigParser()
    config_file=get_config_path()
    config.read(config_file)
    ref = config.get('default', 'schema_ref')
    return ref


#test check_schema_file_exist
@patch('monitor.logger',logging.getLogger('monitor'))
def test_check_schema_file_exist(vel_schema_path,schema_ref):
    result = monitor.check_schema_file_exist(vel_schema_path,schema_ref)
    path=os.getcwd()
    assert result ==os.path.join(path,"collector/evel-test-collector/docs/schema/forge.3gpp.org_rep_sa5_MnS_blob_SA88-Rel16_OpenAPI/faultMnS.yaml")


@pytest.fixture
def wrong_schema_ref():
    config = configparser.ConfigParser()
    config_file=get_wrong_config_path()
    config.read(config_file)
    ref = config.get('default', 'schema_ref')
    return ref



# test check schema file path not exist and checking downloaded file content is yaml or html
@patch('monitor.logger',logging.getLogger('monitor'))
@unittest.mock.patch('os.system')
def test_check_schema_file_content_html(mock_sys,vel_schema_path,wrong_schema_ref):
    f=open("test_faultMns.html","w+")
    f.write("<!DOCTYPE html>")
    f.close()
    path=os.getcwd()
    vel_schema_path=os.path.join(path,"tests/collector/")
    mock_sys.return_value=0
    with pytest.raises(Exception):
        result=monitor.check_schema_file_exist(vel_schema_path,wrong_schema_ref)
        assert result ==os.path.join(path,'tests/collector//forge.3gpp.org_rep_sa5_MnS_blob_SA88-Rel16_OpenAPI/test_faultMns.html')
    # after creating new file its deleted to keep code in first stage
    os.remove(os.path.join(path,"test_faultMns.html"))


@pytest.fixture
def wrong_schema_ref2():
    config = configparser.ConfigParser()
    config_file=get_wrong_config_port_path()
    config.read(config_file)
    ref = config.get('default', 'schema_ref')
    return ref


# test if downloaded file content is yaml Create a folder from source url
@patch('monitor.logger',logging.getLogger('monitor'))
@unittest.mock.patch('os.system')
def test_check_schema_file_path_not_exist_else(mock_sys,vel_schema_path,wrong_schema_ref2):
    f=open("test_faultMns.yaml","w+")
    f.write("NotifyNewAlarm")
    f.close()
    path=os.getcwd()
    vel_schema_path=os.path.join(path,"tests/collector/")
    mock_sys.return_value=0
    result=monitor.check_schema_file_exist(vel_schema_path,wrong_schema_ref2)
    # after running test case, created file is deleted to keep code in first stage
    os.remove(os.path.join(path,"test_faultMns.yaml"))
    assert result==os.path.join(path,'tests/collector//forge.3gpp.org_rep_sa5_MnS_blob_SA88-Rel16_OpenAPI/test_faultMns.yaml')



#test stnd_define_event_validation
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('monitor.check_schema_file_exist')
def test_stnd_define_event_validation(mocker_check,vel_schema_path,body):
    body={"event":{"stndDefinedFields":{"schemaReference":"https://forge.3gpp.org/rep/sa5/MnS/blob/SA88-Rel16/OpenAPI/faultMnS.yaml#components/schemas/NotifyNewAlarm","data":{"href": "href1", "notificationId": 0,"notificationType": "notifyNewAlarm","eventTime": "2022-06-22T12:43:50.579315Z", "systemDN": "xyz","alarmType": "COMMUNICATIONS_ALARM",
         "alarmId": "lossOfSignal","probableCause": "lossOfSignal","specificProblem": "lossOfSignal","perceivedSeverity": "CRITICAL","correlatedNotifications": [],"rootCauseIndicator": False,"backedUpStatus": True,"backUpObject": "xyz","trendIndication": "MORE_SEVERE"}}}}
    path = os.getcwd()
    mocker_check.return_value=os.path.join(path,"collector/evel-test-collector/docs/schema/forge.3gpp.org_rep_sa5_MnS_blob_SA88-Rel16_OpenAPI/faultMnS.yaml")
    result=monitor.stnd_define_event_validation(vel_schema_path,body)
    assert result==None



#check  save_event_in_kafka() function
@mock.patch('monitor.kafka_server')
@mock.patch('monitor.logger', logging.getLogger('monitor'))
def test_save_event_in_kafka(mocker,data_set,topic_name):
    data_set_string=json.dumps(data_set)
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.INFO)
    mocker.patch('monitor.produce_events_in_kafka')
    with mock.patch.object(logger,'info') as mock_info:
        monitor.save_event_in_kafka(data_set_string)
        mock_info.assert_called_once_with('Got an event request for topic domain')


# check save_event_in_kafka() topic length
@patch('monitor.logger',logging.getLogger('monitor'))
@mock.patch('monitor.produce_events_in_kafka')
@mock.patch('monitor.kafka_server')
def test_save_event_in_kafka_topic_len(server,mock_producer,topic_name):
    body={'event':{'commonEventHeader':{'domain':''}}}
    body=json.dumps(body)
    monitor.save_event_in_kafka(body)
    data_set={'event': {'commonEventHeader': {'domain': ''}}}
    mock_producer.assert_called_once_with(data_set,'')



#check produce_event_in_kafka() function      
@mock.patch('monitor.KafkaProducer')
@mock.patch('monitor.producer')
@mock.patch('monitor.logger', logging.getLogger('monitor'))
def test_produce_events_in_kafka(mock_pro,mock_producer,data_set,topic_name):
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    with mock.patch.object(logger,'debug') as mock_debug:
        monitor.produce_events_in_kafka(data_set,topic_name)
        mock_pro.send.assert_called_with(topic_name,value=data_set)
        mock_debug.assert_called_once_with('Event has been successfully posted into kafka bus')
        path=os.getcwd()
        os.remove(os.path.join(path,'collector.log'))



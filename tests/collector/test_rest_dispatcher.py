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
import logging
import rest_dispatcher
from gevent import socket
from gevent import pywsgi


@pytest.fixture
def start_response():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_response = pywsgi.WSGIHandler(sock, "", "")
    return start_response


# test test_notfound_404
@patch("rest_dispatcher.base_url", "")
@mock.patch("gevent.pywsgi.Input", autospec=True)
@mock.patch("rest_dispatcher.set_404_content")
def test_notfound_404(mocker_dispatcher, mock_input, start_response):
    environ = {"REQUEST_METHOD": "POST", "PATH_INFO": ""}
    mock_start_response = mock.Mock(start_response)
    logger = logging.getLogger("monitor")
    logger.setLevel(logging.DEBUG)
    with mock.patch.object(logger, "debug") as mock_debug:
        result = rest_dispatcher.notfound_404(environ, mock_start_response)
        assert result == ["template_404"]


# test call of
@patch("rest_dispatcher.base_url", "")
@mock.patch("gevent.pywsgi.Input", autospec=True)
def test_call(mock_input, start_response):
    environ = {"REQUEST_METHOD": "POST", "PATH_INFO": ""}
    mock_start_response = mock.Mock(start_response)
    rest_obj = rest_dispatcher.PathDispatcher()
    res = rest_obj.__call__(environ, mock_start_response)
    assert ["template_404"] == res


@patch("rest_dispatcher.base_url")
def test_set_404_content(mock_url):
    mock_url.return_value = ""
    result = rest_dispatcher.set_404_content("")
    assert result == None


@pytest.fixture
def path():
    path = "/eventListener/v7/events"
    return path


@pytest.fixture
def method():
    method = "post"
    return method


def test_register(path, method):
    rest_obj = rest_dispatcher.PathDispatcher()
    res = rest_obj.register(path, method, None)
    assert res == None

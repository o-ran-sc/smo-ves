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

import argparse
import os
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import configparser
from unittest import mock
from unittest.mock import patch
from pytest_mock import MockerFixture
import logging
from app_config import AppConfig
import pytest

def get_path():
    project_path = os.getcwd()
    return project_path

def get_config_path():
    project_path=get_path()
    config_path = os.path.join(
    project_path,"dmaapadapter/adapter/config/adapter.conf")
    return config_path

@pytest.fixture
def kafkaBroker():
    kafkaBroker='broker'
    return kafkaBroker

@pytest.fixture
def logger():
    logger = logging.getLogger('DMaaP')
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    return logger

@pytest.fixture
def enable_assert():
    assert_value='enable'
    return assert_value


#test init function in appconfig
@mock.patch('app_config.AppConfig.setLogger')
@mock.patch('argparse.ArgumentParser.parse_args',
return_value=argparse.Namespace(config=get_config_path(),section='default'))
def test___init__(parser,mock_setLogger):
    AppConfig.__init__(AppConfig)
    mock_setLogger.assert_called_with('dmaap.log','error')


#test kafka broker
def test_getKafkaBroker(kafkaBroker):
    AppConfig.kafka_broker=kafkaBroker
    res=AppConfig.getKafkaBroker(AppConfig)
    assert res == kafkaBroker

#test getLogger
def test_getLogger(logger):
    AppConfig.logger=logger
    res=AppConfig.getLogger(AppConfig)
    assert res.getEffectiveLevel()==20


#test logger level Info
def test_setLogger(logger):
    log_file= 'dmaap.log'
    log_level='INFO'
    with mock.patch.object(logger,'info') as mock_info:
        AppConfig.setLogger(AppConfig,log_file,log_level)
        mock_info.assert_called_with('Log level INFO and log file dmaap.log : ')


#test setLogger Debug
def test_setLogger_debug(logger):
    log_file= 'dmaap.log'
    log_level= 'DEBUG'
    with mock.patch.object(logger,'info') as mock_debug:
        AppConfig.setLogger(AppConfig,log_file,log_level)
        mock_debug.assert_called_with('Log level DEBUG and log file dmaap.log : ')


#test setLogger error
def test_setLogger_error(logger):
    log_file= 'dmaap.log'
    log_level='ERROR'
    with mock.patch.object(logger,'info') as mock_error:
        AppConfig.setLogger(AppConfig,log_file,log_level)
        mock_error.assert_called_with('Log level ERROR and log file dmaap.log : ')

        

#test AssertConfigValue
def test_getAssertConfigValue(enable_assert):
    AppConfig.enable_assert=enable_assert
    res=AppConfig.getAssertConfigValue(AppConfig)
    assert res==enable_assert

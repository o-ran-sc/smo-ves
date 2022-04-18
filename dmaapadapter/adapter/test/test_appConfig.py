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
    project_path = project_path[:project_path.rfind('/')]
    return project_path

def get_config_path():
    project_path=get_path()
    config_path = os.path.join(
    project_path,"config/adapter.conf")
    return config_path

@pytest.fixture
def kafkaBroker():
    kafkaBroker='broker'
    return kafkaBroker

@pytest.fixture
def logger():
    logger = logging.getLogger('DMaaP')
    logger.setLevel(logging.INFO)
    return logger

@mock.patch('app_config.AppConfig.setLogger')
@mock.patch('argparse.ArgumentParser.parse_args',
return_value=argparse.Namespace(config=get_config_path(),section='default'))
def test___init__(parser,mock_setLogger):
    AppConfig.__init__(AppConfig)
    mock_setLogger.assert_called_with('dmaap.log','error')

def test_getKafkaBroker(kafkaBroker):
     AppConfig.kafka_broker=kafkaBroker
     res=AppConfig.getKafkaBroker(AppConfig)
     assert res == kafkaBroker

def test_getLogger(logger):
     AppConfig.logger=logger
     res=AppConfig.getLogger(AppConfig)
     assert res.getEffectiveLevel()==20

def test_setLogger(logger):
    log_file= 'dmaap.log'
    log_level='INFO'
    with mock.patch.object(logger,'info') as mock_info:
        AppConfig.setLogger(AppConfig,log_file,log_level)
        mock_info.assert_called_with('Log level INFO and log file dmaap.log : ')

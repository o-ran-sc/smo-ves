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

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import configparser
import logging.handlers


class AppConfig:
    kafka_broker = ""
    logger = logging.getLogger()

    def __init__(self):
        parser = ArgumentParser(description="",
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-c', '--config',
                            dest='config',
                            default='/opt/ves/adapter/config/adapter.conf',
                            help='Use this config file.')
        parser.add_argument('-s', '--section',
                            dest='section',
                            default='default',
                            metavar='<section>',
                            help='section to use in the config file')

        args = parser.parse_args()
        config_file = args.config
        config_section = args.section

        overrides = {}
        config = configparser.ConfigParser()
        config.read(config_file)

        self.kafka_broker = config.get(config_section,
                                       'kafka_broker',
                                       vars=overrides)
        log_file = config.get(config_section, 'log_file', vars=overrides)
        log_level = config.get(config_section, 'log_level', vars=overrides)

        handler = logging.handlers.RotatingFileHandler(log_file,
                                                       maxBytes=1000000,
                                                       backupCount=10)
        formatter = logging.Formatter('%(asctime)s %(name)s - '
                                      '%(levelname)s - %(message)s',
                                      '%Y-%m-%d %H:%M:%S.%f %z')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # we are going to set the log level
        if (log_level == 'DEBUG'):
            self.logger.setLevel(logging.DEBUG)
        elif (log_level == 'ERROR'):
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)

        self.logger.info('Log level {} and log file {} : '
                         .format(log_level, log_file))

    def getKafkaBroker(self):
        return self.kafka_broker

    def getLogger(self):
        return self.logger

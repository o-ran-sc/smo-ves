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

from confluent_kafka.admin import AdminClient, KafkaException
from confluent_kafka import Consumer
from app_config import AppConfig
import logging
import sys


class EventConsumer:
    broker = ""
    logger = logging.getLogger()

    def __init__(self):
        appConfig = AppConfig()
        self.logger = appConfig.getLogger()
        self.broker = appConfig.getKafkaBroker()

    def consumeEvents(self, topic, consumergroup, consumerid, limit, timeout):
        self.logger.debug("topic={}, consumergroup={}, consumerid={}, limit={}, timeout={} "
                          .format(topic, consumergroup, consumerid, limit, timeout))
        consumer_config = {
            'bootstrap.servers': self.broker,
            'group.id': consumergroup,
            'group.instance.id': consumerid,
            'auto.offset.reset': 'largest',
            'enable.auto.commit': 'false'
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])
        event_list = []

        try:
            ctr = 0
            content_size = 0
            while True:
                if (ctr == int(limit)):
                    break
                if(content_size > 300000):
                    break
                ctr += 1
                # read single message at a time
                msg = consumer.poll(timeout=int(timeout))
                if msg is None:
                    self.logger.debug("No records ")
                    break
                if msg.error():
                    self.logger.dubug("Error reading message : {}".format(msg.error()))
                    break

                content_size = content_size + sys.getsizeof(msg.value().decode('utf8').replace("'", '"'))
                event_list.append(msg.value().decode('utf8').replace("'", '"'))
                consumer.commit()

        except Exception as ex:
            self.logger.debug('Failed to get event information due to unexpected reason! {0}'.format(ex))

        finally:
            self.logger.debug("closing consumer")
            consumer.close()
            return event_list


class TopicConsumer:

    broker = ""
    logger = logging.getLogger()
    timeout = 10

    def __init__(self):
        appConfig = AppConfig()
        self.logger = appConfig.getLogger()
        self.broker = appConfig.getKafkaBroker()

    def getTopics(self):
        try:
            adminClient = AdminClient({"bootstrap.servers": self.broker})
            ListTopicsResult = adminClient.list_topics(timeout=self.timeout)
            topic_list = []

            for key, value in ListTopicsResult.topics.items():
                topic_list.append(key)

            dict = {'topics':topic_list}
            return dict

        except Exception as ex:
            self.logger.debug('Failed to get topic information due to unexpected reason! {0}'.format(ex))

    def listAllTopics(self):
        try:
            topic_list = []
            adminClient = AdminClient({"bootstrap.servers": self.broker})
            ListTopicsResult = adminClient.list_topics(timeout=self.timeout)

            for key, value in ListTopicsResult.topics.items():
                dict = {'topicName':key, 'owner' : '', 'txenabled' : False}
                topic_list.append(dict)

            dict2 = {'topics':topic_list}
            return dict2
        except Exception as ex:
            self.logger.debug('Failed to get list of topic information due to unexpected reason! {0}'.format(ex))


    def getTopicDetails(self, topic):
        try:
            adminClient = AdminClient({"bootstrap.servers": self.broker})
            ListTopicsResult = adminClient.list_topics(timeout=self.timeout)

            for key, value in ListTopicsResult.topics.items():
                if (key == topic):
                    dict = {'name':key, 'owner' : '', 'description' : '', 'readerAcl' : {"enabled": True,
                                "users": []}, 'writerAcl' : {"enabled": True,"users": []}}
                    return dict

            self.logger.debug("Topic {} does not exists! ".format(topic))
            return "Topic [" + topic+ "] does not exists"
        except Exception as ex:
            self.logger.debug('Failed to get topic detail due to unexpected reason! {0}'.format(ex))



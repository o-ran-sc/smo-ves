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

import flask
from flask import request
from consumer import EventConsumer, TopicConsumer
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api_base_url = "/dmaapapi/v1/"


@app.route("/")
def index():
    return "Welcome !!"


@app.route(api_base_url + '/topics', methods=['GET'])
def get_all_topics():
    topicConsumer = TopicConsumer()
    response = app.response_class(response=json.dumps(topicConsumer.getTopics()),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route(api_base_url + '/topics/listAll', methods=['GET'])
def listall_topics():
    topicConsumer = TopicConsumer()
    response = app.response_class(response=json.dumps(topicConsumer.listAllTopics()),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route(api_base_url + '/topics/<topic>', methods=['GET'])
def topic_details(topic):
    assert topic == request.view_args['topic']
    topicConsumer = TopicConsumer()
    response = app.response_class(response=json.dumps(topicConsumer.getTopicDetails(topic)),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route(api_base_url + '/events/<topic>/<consumergroup>/<consumerid>', methods=['GET'])
def get_events(topic, consumergroup, consumerid):
    assert topic == request.view_args['topic']
    assert consumergroup == request.view_args['consumergroup']
    assert consumerid == request.view_args['consumerid']
    limit = ""
    timeout = ""

    if 'limit' in request.args:
        limit = request.args['limit']
    if 'timeout' in request.args:
        timeout = request.args['timeout']

    eventConsumer = EventConsumer()
    response = app.response_class(response=json.dumps(
                                    eventConsumer.consumeEvents(
                                        topic,
                                        consumergroup,
                                        consumerid,
                                        getLimit(limit),
                                        getTimeout(timeout))),
                                  status=200,
                                  mimetype='application/json')
    return response


def getLimit(limit):
    try:
        limit = int(limit)
    except Exception:
        limit = -1
    finally:
        return limit


def getTimeout(timeout):
    try:
        timeout = int(timeout)
    except Exception:
        timeout = 15
    finally:
        return timeout


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

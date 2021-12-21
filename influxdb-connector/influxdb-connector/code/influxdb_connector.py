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
import sys
import os
import platform
import json
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import configparser
import logging.handlers
import requests
import urllib.request as url
from confluent_kafka import Consumer, KafkaError

# ------------------------------------------------------------------------------
# Address of influxdb server.
# ------------------------------------------------------------------------------

influxdb = '127.0.0.1'

logger = None

def send_to_influxdb(event, pdata):
    url = 'http://{}/write?db=eventsdb'.format(influxdb)
    logger.debug('Send {} to influxdb at {}: {}'.format(event, influxdb, pdata))
    r = requests.post(url, data=pdata, headers={'Content-Type': 'text/plain'})
    logger.info('influxdb return code {}'.format(r.status_code))
    if r.status_code != 204:
         logger.debug('*** Influxdb save failed, return code {} ***'.format(r.status_code))

def process_additional_measurements(val, domain, eventId, startEpochMicrosec, lastEpochMicrosec):
    for additionalMeasurements in val:
        pdata = domain + ",eventId={},system={}".format(eventId, source)
        nonstringpdata = " startEpochMicrosec={},lastEpochMicrosec={},".format(startEpochMicrosec, lastEpochMicrosec)
        for key, val in additionalMeasurements.items():
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            elif isinstance(val, dict):
                for key2, val2 in val.items():
                    if isinstance(val2, str):
                        pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                    else:
                        nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)
    send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_nonadditional_measurements(val, domain, eventId, startEpochMicrosec, lastEpochMicrosec):
    for disk in val:
        pdata = domain + ",eventId={},system={}".format(eventId, source)
        nonstringpdata = " startEpochMicrosec={},lastEpochMicrosec={},".format(startEpochMicrosec, lastEpochMicrosec)
        for key, val in disk.items():
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)

        send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_pnfRegistration_event(domain, jobj, pdata, nonstringpdata):
    pdata = pdata + ",system={}".format(source)
    for key, val in jobj.items():
        if key != 'additionalFields' and val != "":
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)
        elif key == 'additionalFields':
            for key2, val2 in val.items():
                if val2 != "" and isinstance(val2, str):
                    pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                elif val2 != "":
                    nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)

    send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_thresholdCrossingAlert_event(domain, jobj, pdata, nonstringpdata):
    pdata = pdata + ",system={}".format(source)
    for key, val in jobj.items():
        if (key != 'additionalFields' and key != 'additionalParameters' and key != 'associatedAlertIdList') and val != "":
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)
        elif key == 'additionalFields':
            for key2, val2 in val.items():
                if val2 != "" and isinstance(val2, str):
                    pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                elif val2 != "":
                    nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)
        elif key == 'additionalParameters':
            for addParameter in val:
                for key2, val2 in addParameter.items():
                    if key2 != "hashMap":
                        if val2 != "" and isinstance(val2, str):
                            pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                        elif val2 != "":
                            nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)
                    elif key2 == "hashMap":
                        for key3, val3 in val2.items():
                            if val3 != "" and isinstance(val3, str):
                                pdata = pdata + ',{}={}'.format(key3, process_special_char(val3))
                            elif val3 != "":
                                nonstringpdata = nonstringpdata + '{}={},'.format(key3, val3)
        elif key == 'associatedAlertIdList':
            associatedAlertIdList = ""
            for associatedAlertId in val:
                associatedAlertIdList = associatedAlertIdList + associatedAlertId + "|"
                if(associatedAlertIdList != ""):
                    pdata = pdata + ',{}={}'.format("associatedAlertIdList",
                                                    process_special_char(associatedAlertIdList)[:-1])

    send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_fault_event(domain, jobj, pdata, nonstringpdata):
    pdata = pdata + ",system={}".format(source)
    for key, val in jobj.items():
        if key != 'alarmAdditionalInformation' and val != "":
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)
        elif key == 'alarmAdditionalInformation':
            for key2, val2 in val.items():
                if val2 != "" and isinstance(val2, str):
                    pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                elif val2 != "":
                    nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)

    send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_heartbeat_events(domain, jobj, pdata, nonstringpdata):
    pdata = pdata + ",system={}".format(source)
    for key, val in jobj.items():
        if key != 'additionalFields' and val != "":
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)
        elif key == 'additionalFields':
            for key2, val2 in val.items():
                if val2 != "" and isinstance(val2, str):
                    pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                elif val2 != "":
                    nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)

    send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_measurement_events(domain, jobj, pdata, nonstringpdata, eventId, startEpochMicrosec, lastEpochMicrosec):
    pdata = pdata + ",system={}".format(source)
    for key, val in jobj.items():
        if val != "":
            if isinstance(val, str):
                pdata = pdata + ',{}={}'.format(key, process_special_char(val))
            elif isinstance(val, list):
                if key == 'additionalMeasurements':
                    process_additional_measurements(val, domain + "additionalmeasurements", eventId, startEpochMicrosec, lastEpochMicrosec)
                elif key == 'cpuUsageArray':
                    process_nonadditional_measurements(val, domain + "cpuusage", eventId, startEpochMicrosec, lastEpochMicrosec)
                elif key == 'diskUsageArray':
                    process_nonadditional_measurements(val, domain + "diskusage", eventId, startEpochMicrosec, lastEpochMicrosec)
                elif key == 'memoryUsageArray':
                    process_nonadditional_measurements(val, domain + "memoryusage", eventId, startEpochMicrosec, lastEpochMicrosec)
                elif key == 'nicPerformanceArray':
                    process_nonadditional_measurements(val, domain + "nicperformance", eventId, startEpochMicrosec, lastEpochMicrosec)
                elif key == 'loadArray':
                    process_nonadditional_measurements(val, domain + "load", eventId, startEpochMicrosec, lastEpochMicrosec)
                elif key == 'networkSliceArray':
                    process_nonadditional_measurements(val, domain + "networkslice", eventId, startEpochMicrosec, lastEpochMicrosec)
            elif isinstance(val, dict):
                for key2, val2 in val.items():
                    if isinstance(val2, str):
                        pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                    else:
                        nonstringpdata = nonstringpdata + '{}={},'.format(key2, val2)
            else:
                nonstringpdata = nonstringpdata + '{}={},'.format(key, val)

    send_to_influxdb(domain, pdata + nonstringpdata[:-1] + ' ' + process_time(eventTimestamp))


def process_special_char(str):
    for search_char, replace_char in {" ": "\ ", ",": "\,"}.items():
        str = str.replace(search_char, replace_char)
    return str


def process_time(eventTimestamp):
    eventTimestamp = str(eventTimestamp).replace(".", "")
    while len(eventTimestamp) < 19:
        eventTimestamp = eventTimestamp + "0"
    return format(int(eventTimestamp))


def save_event_in_db(body):
    jobj = json.loads(body)
    global source
    global eventTimestamp
    source = "unknown"

    domain = jobj['event']['commonEventHeader']['domain']
    eventTimestamp = jobj['event']['commonEventHeader']['startEpochMicrosec']
    agent = jobj['event']['commonEventHeader']['reportingEntityName'].upper()
    if "LOCALHOST" in agent:
        agent = "computehost"
        source = jobj['event']['commonEventHeader']['sourceId'].upper()

    # processing common header part
    pdata = domain

    nonstringpdata = " "
    commonHeaderObj = jobj['event']['commonEventHeader'].items()
    for key, val in commonHeaderObj:
        if val != "":
            if (key != 'internalHeaderFields'):
                if isinstance(val, str):
                    pdata = pdata + ',{}={}'.format(key, process_special_char(val))
                else:
                    nonstringpdata = nonstringpdata + '{}={}'.format(key, val) + ','
            if (key == 'internalHeaderFields'):
                for key2, val2 in val.items():
                    if val2 != "":
                        if isinstance(val2, str):
                            pdata = pdata + ',{}={}'.format(key2, process_special_char(val2))
                        else:
                            nonstringpdata = nonstringpdata + '{}={}'.format(key2, val2) + ','

    # processing pnfRegistration events
    if 'pnfRegistrationFields' in jobj['event']:
        logger.debug('Found pnfRegistrationFields')
        process_pnfRegistration_event(domain,
                                      jobj['event']['pnfRegistrationFields'],
                                      pdata,
                                      nonstringpdata)

    # processing thresholdCrossingAlert events
    if 'thresholdCrossingAlertFields' in jobj['event']:
        logger.debug('Found thresholdCrossingAlertFields')
        process_thresholdCrossingAlert_event(domain,
                                             jobj['event']['thresholdCrossingAlertFields'],
                                             pdata,
                                             nonstringpdata)

    # processing fault events
    if 'faultFields' in jobj['event']:
        logger.debug('Found faultFields')
        process_fault_event(domain, jobj['event']['faultFields'], pdata, nonstringpdata)

    # process heartbeat events
    if 'heartbeatFields' in jobj['event']:
        logger.debug('Found Heartbeat')
        process_heartbeat_events(domain,
                                 jobj['event']['heartbeatFields'],
                                 pdata,
                                 nonstringpdata)

    # processing measurement events
    if 'measurementFields' in jobj['event']:
        logger.debug('Found measurementFields')
        process_measurement_events(domain,
                                   jobj['event']['measurementFields'],
                                   pdata,
                                   nonstringpdata,
                                   jobj['event']['commonEventHeader']['eventId'],
                                   jobj['event']['commonEventHeader']['startEpochMicrosec'],
                                   jobj['event']['commonEventHeader']['lastEpochMicrosec'])


def main():

    # ----------------------------------------------------------------------
    # Setup argument parser so we can parse the command-line.
    # ----------------------------------------------------------------------
    parser = ArgumentParser(description='',
                               formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--influxdb',
                            dest='influxdb',
                            default='localhost',
                            help='InfluxDB server addresss')
    parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            action='count',
                            help='set verbosity level')
    parser.add_argument('-c', '--config',
                            dest='config',
                            default='/opt/smo/connector/config/consumer.conf',
                            help='Use this config file.',
                            metavar='<file>')
    parser.add_argument('-s', '--section',
                            dest='section',
                            default='default',
                            metavar='<section>',
                            help='section to use in the config file')

    # ----------------------------------------------------------------------
    # Process arguments received.
    # ----------------------------------------------------------------------
    args = parser.parse_args()
    config_file = args.config
    verbose = args.verbose
    config_section = args.section

    # ----------------------------------------------------------------------
    # Now read the config file, using command-line supplied values as
    # overrides.
    # ----------------------------------------------------------------------
    overrides = {}
    config = configparser.ConfigParser()
    config['defaults'] = {'log_file': 'influxdbConnector.log'
                          }
    config.read(config_file)


    # ----------------------------------------------------------------------
    # extract the values we want.
    # ----------------------------------------------------------------------

    global influxdb
    global kafka_server

    influxdb = config.get(config_section, 'influxdb', vars=overrides)
    log_file = config.get(config_section, 'log_file', vars=overrides)
    kafka_server=config.get(config_section,'kafka_server',
                                   vars=overrides)

    # ----------------------------------------------------------------------
    # Finally we have enough info to start a proper flow trace.
    # ----------------------------------------------------------------------
    global logger
    logger = logging.getLogger('monitor')

    if ((verbose is not None) and (verbose > 0)):
        logger.info('Verbose mode on')
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(log_file,
                                                       maxBytes=1000000,
                                                       backupCount=10)
    if (platform.system() == 'Windows'):
        date_format = '%Y-%m-%d %H:%M:%S'
    else:
        date_format = '%Y-%m-%d %H:%M:%S.%f %z'
        formatter = logging.Formatter('%(asctime)s %(name)s - '
                                      '%(levelname)s - %(message)s',
                                      date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Started')
    # ----------------------------------------------------------------------
    # Log the details of the configuration.
    # ----------------------------------------------------------------------
    logger.debug('Log file = {0}'.format(log_file))
    logger.debug('Influxdb server = {0}'.format(influxdb))
    logger.debug('kafka server = {0}'.format(kafka_server))

    # ----------------------------------------------------------------------
    # kafka Consumer code .
    # ----------------------------------------------------------------------


    settings = {
        'bootstrap.servers': kafka_server,
        'group.id': 'mygroup',
        'client.id': 'client-1',
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'earliest'}
    }

    c = Consumer(settings)

    c.subscribe(['measurement','pnfregistration',
    'fault','thresholdcrossingalert','heartbeat'])

    try:
        while True:
            msg = c.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                logger.debug('Recived message from topic name {} and offset number {}'.format(msg.topic(), msg.offset()))
                # saving data in influxdb
                save_event_in_db(msg.value())
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                logger.error('End of partition reached {0}/{1}'
                      .format(msg.topic(), msg.partition()))
            else:
                logger.error('Error occured: {0}'.format(msg.error().str()))

    except KeyboardInterrupt:
        pass

    finally:
        c.close()

if __name__ == '__main__':
    main()

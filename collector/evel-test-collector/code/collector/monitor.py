#!/usr/bin/env python
#
# Original work Copyright 2016-2017 AT&T Intellectual Property, Inc
# Modified work Copyright 2021 Xoriant Corporation
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
# What this is: Monitor and closed-loop policy agent as part of the OPNFV VES
# ves_onap_demo.
#
# Status: this is a work in progress, under test.

from rest_dispatcher import PathDispatcher, set_404_content
from wsgiref.simple_server import make_server
import sys
import os
import platform
import traceback
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import configparser
import logging.handlers
from base64 import b64decode
import json
import jsonschema
from functools import partial
from datetime import timezone
from kafka import KafkaProducer
from json import dumps
import datetime
import time
from gevent import pywsgi
import yaml
import requests

monitor_mode = "f"
vdu_id = ['', '', '', '', '', '']
summary_e = ['***** Summary of key stats *****', '', '', '']
summary_c = ['Collectd agents:']
status = ['', 'Started', 'Started', 'Started']
base_url = ''
template_404 = b'''POST {0}'''
columns = 0
rows = 0


class JSONObject:

    def __init__(self, d):
        self.__dict__ = d


__all__ = []
__version__ = 0.1
__date__ = '2015-12-04'
__updated__ = '2015-12-04'

TESTRUN = False
DEBUG = False
PROFILE = False

# ------------------------------------------------------------------------------
# Credentials we expect clients to authenticate themselves with.
# ------------------------------------------------------------------------------
vel_username = ''
vel_password = ''

# ------------------------------------------------------------------------------
# The JSON schema which we will use to validate events.
# ------------------------------------------------------------------------------
vel_schema = None

#------------------------------------------------------------------------------
# The yaml schema which we will use to validate events.
# ------------------------------------------------------------------------------
vel_yaml_schema = None

# ------------------------------------------------------------------------------
# The JSON schema which we will use to validate client throttle state.
# ------------------------------------------------------------------------------
throttle_schema = None

# ------------------------------------------------------------------------------
# The JSON schema which we will use to provoke throttling commands for testing.
# ------------------------------------------------------------------------------
test_control_schema = None

# ------------------------------------------------------------------------------
# Pending command list from the testControl API
# This is sent as a response commandList to the next received event.
# ------------------------------------------------------------------------------
pending_command_list = None

# ------------------------------------------------------------------------------
# Logger for this module.
# ------------------------------------------------------------------------------
logger = None
producer = None


def listener(environ, start_response, schema, yaml_schema=None):
    '''
    Handler for the Vendor Event Listener REST API.

    Extract headers and the body and check that:

      1)  The client authenticated themselves correctly.
      2)  The body validates against the provided schema for the API.

    '''
    logger.info('Got a Vendor Event request')
    logger.info('==== ' + time.asctime() + ' ' + '=' * 49)

    # --------------------------------------------------------------------------
    # GET request.
    # --------------------------------------------------------------------------
    if environ.get('REQUEST_METHOD') == 'GET':
        start_response('200 OK', [('Content-type', 'text/plain')])
        yield ('POST  ' + get_info).encode()
        return

    # --------------------------------------------------------------------------
    # Extract the content from the request.
    # --------------------------------------------------------------------------
    length = int(environ.get('CONTENT_LENGTH', '0'))
    logger.debug('Content Length: {0}'.format(length))
    body = environ['wsgi.input'].read(length)
    logger.debug('Content Body: {0}'.format(body))

    mode, b64_credentials = str.split(environ.get('HTTP_AUTHORIZATION',
                                      'None None'))
    logger.debug('Auth. Mode: {0} Credentials: ****'.format(mode))
    if (b64_credentials != 'None'):
        credentials = b64decode(b64_credentials)
    else:
        credentials = None

    logger.debug('Credentials: ****')

    # --------------------------------------------------------------------------
    # If we have a schema file then check that the event matches that expected.
    # --------------------------------------------------------------------------
    if (schema is not None):
        logger.debug('Attempting to validate data: {0}\n'
                     'Against schema: {1}'.format(body, schema))
        try:
            decoded_body = json.loads(body)
            validate = jsonschema.validate(decoded_body, schema)
            assert (validate is None), "Invalid event!"
            if 'stndDefinedFields' in decoded_body['event'].keys():
                logger.debug('in yaml validation')
                schema_ref = decoded_body['event']['stndDefinedFields']["schemaReference"]
                if "https://forge.3gpp.org"  in schema_ref or "https://gerrit.o-ran-sc.org" in schema_ref:
                    stnd_define_event_validation(yaml_schema, decoded_body)
                else :
                    logger.error("schema reference {0} not supported.".format(schema_ref))
                    raise Exception("schema reference {0} not supported.".format(schema_ref))

            logger.info('Event is valid!')
            logger.info('Valid body decoded & checked against schema OK:\n'
                        '{0}'.format(json.dumps(decoded_body,
                                     sort_keys=True,
                                     indent=4,
                                     separators=(',', ': '))))
    # --------------------------------------------------------------------------
    # See whether the user authenticated themselves correctly.
    # --------------------------------------------------------------------------
            if (credentials == bytes((vel_username + ':' + vel_password),
                                     'utf-8')):
                logger.info('Authenticated OK')

        # ----------------------------------------------------------------------
        # Respond to the caller. If we have a pending commandList from the
        # testControl API, send it in response.
        # ----------------------------------------------------------------------
                global pending_command_list
                if pending_command_list is not None:
                    start_response('202 Accepted',
                                   [('Content-type', 'application/json')])
                    response = pending_command_list
                    pending_command_list = None

                    logger.debug('\n' + '=' * 80)
                    logger.debug('Sending pending commandList in the response:\n'
                                 '{0}'.format(json.dumps(response,
                                              sort_keys=True,
                                              indent=4,
                                              separators=(',', ': '))))
                    logger.debug('=' * 80 + '\n')
                    yield json.dumps(response).encode()
                else:
                    start_response('202 Accepted', [])
                    yield ''.encode()
            else:
                logger.warn('Failed to authenticate OK; creds: ' , credentials)
                logger.warn('Failed to authenticate agent credentials: ',
                            credentials,
                            'against expected ',
                            vel_username,
                            ':',
                            vel_password)

        # ----------------------------------------------------------------------
        # Respond to the caller.
        # ----------------------------------------------------------------------
                start_response('401 Unauthorized', [('Content-type',
                                                     'application/json')])
                req_error = {'requestError': {
                                 'policyException': {
                                    'messageId': 'POL0001',
                                    'text': 'Failed to authenticate'
                                    }
                                 }
                             }
                yield json.dumps(req_error)

            # saving data in Kafka by deafult
            save_event_in_kafka(body)

        except jsonschema.SchemaError as e:
            logger.error('Schema is not valid! {0}'.format(e))
            # Stop container forcefully.
            os._exit(0)
        except jsonschema.ValidationError as e:
            logger.warn('Event is not valid against schema! {0}'.format(e))
            logger.warn('Bad JSON body decoded:\n'
                        '{0}'.format(json.dumps(decoded_body,
                                     sort_keys=True,
                                     indent=4,
                                     separators=(',', ': '))))
            start_response('400 Bad Request',
                                   [('Content-type', 'application/json')])
            yield ''.encode()
        except Exception as e:
            logger.error('Event invalid for unexpected reason! {0}'.format(e))
            start_response('500 Internal Server Error',
                                   [('Content-type', 'application/json')])
            yield ''.encode()
    else:
        logger.debug('No schema so just decode JSON: {0}'.format(body))
        try:
            decoded_body = json.loads(body)
            logger.warn('Valid JSON body (no schema checking) decoded:\n'
                        '{0}'.format(json.dumps(decoded_body,
                                                sort_keys=True,
                                                indent=4,
                                                separators=(',', ': '))))
            logger.warn('Event is valid JSON but not checked against schema!')

        except Exception as e:
            logger.error('Event invalid for unexpected reason! {0}'.format(e))

# --------------------------------------------------------------------------
# check yaml schema file exists or not
# --------------------------------------------------------------------------
def check_schema_file_exist(vel_schema_path, schema_ref):
    logger.debug('in check yaml file')
    assert (vel_schema_path != ""), "Value of property 'schema_file' is missing in config file"
    # Fetching file and folder name from url
    schema_ref =  schema_ref.split('#')[0]
    name_list = schema_ref.split('/')
    folder_name = '_'.join(name_list[2:-1])
    file_name = name_list[-1]
    updated_vel_schema_path = vel_schema_path +'/{0}/{1}'.format(folder_name,file_name)
    if "https://forge.3gpp.org" in schema_ref:
        schema_ref = schema_ref.replace("blob","raw")
        schema_ref =  schema_ref + '?inline=false'
    if not os.path.exists(updated_vel_schema_path):
        logger.warning('Event Listener Schema File ({0}) not found. ''No validation will be undertaken.'.format(vel_schema_path))
        logger.info('Start downloading yaml file :{}'.format(schema_ref))
        result = os.system('curl -JOL "{0}"'.format(schema_ref))
        logger.debug("result {0}".format(result))
        assert(result == 0), "Invalid URL {0}".format(schema_ref)
        logger.info("Download Completed")
        with open(file_name, "r") as file:
            first_line = file.readline()
        # checking downloaded file content is yaml or html
        if first_line.strip() == "<!DOCTYPE html>":
            logger.info("Downloaded file is not valid yaml")
            os.system("del {0} ".format(file_name))
            logger.info("Downloaded file deleted")
            assert(first_line.strip() != "<!DOCTYPE html>"), "Invalid Schema File"
        else:
            # Create a folder from source url
            os.system('mkdir {0}/{1}'.format(vel_schema_path, folder_name))
            # move downloaded file in above created folder
            os.system("mv {0} {1}/{2}".format(file_name, vel_schema_path, folder_name))
    return updated_vel_schema_path

# --------------------------------------------------------------------------
# Second level of validation for stnd define message
# --------------------------------------------------------------------------
def stnd_define_event_validation(schema_path , body):
    logger.debug('in second level validation ')
    schema_ref = body['event']['stndDefinedFields']["schemaReference"]
    schema_path = check_schema_file_exist(schema_path , schema_ref)
    logger.debug('end check yaml path ')
    schema = yaml.full_load(open(schema_path, 'r'))
    schema_name= schema_ref.split('/')[-1]
    updated_schema = dict(schema["components"]["schemas"][schema_name],  **schema)
    decoded_body = body['event']['stndDefinedFields']['data']
    validate_yaml = jsonschema.validate(decoded_body,updated_schema)
    assert(validate_yaml is None), "Invalid event!"
    logger.info('standard defined event validated sucessfully ')
    return validate_yaml
# --------------------------------------------------------------------------
# Save event data in Kafka
# --------------------------------------------------------------------------
def save_event_in_kafka(body):
    jobj = json.loads(body)
    if 'commonEventHeader' in jobj['event']:
        # store each domain information in individual topic
        topic = jobj['event']['commonEventHeader']['domain'].lower()
        logger.info('Got an event request for {} domain'.format(topic))
        if (len(topic) == 0):
            topic = kafka_topic

        logger.debug('Kafka broker ={} and kafka topic={}'.format(kafka_server, topic))
        produce_events_in_kafka(jobj, topic)


def produce_events_in_kafka(jobj, topic):
    try:
        global producer
        if producer is None:
            logger.debug('Producer is None')
            producer = KafkaProducer(bootstrap_servers=[kafka_server],
                                     value_serializer=lambda x:
                                     dumps(x).encode('utf-8'))
        producer.send(topic, value=jobj)
        logger.debug('Event has been successfully posted into kafka bus')
    except Exception as e:
        logger.error('Getting error while posting event into kafka bus {0}'.format(e))


def test_listener(environ, start_response, schema):
    '''
    Handler for the Test Collector Test Control API.

    There is no authentication on this interface.

    This simply stores a commandList which will be sent in response to the next
    incoming event on the EVEL interface.
    '''
    global pending_command_list
    global decoded_body
    logger.info('Got a Test Control input')
    logger.info('============================')
    logger.info('==== TEST CONTROL INPUT ====')

    # --------------------------------------------------------------------------
    # GET allows us to get the current pending request.
    # --------------------------------------------------------------------------
    if environ.get('REQUEST_METHOD') == 'GET':
        start_response('200 OK', [('Content-type', 'application/json')])
        yield json.dumps(pending_command_list)
        return

    # --------------------------------------------------------------------------
    # Extract the content from the request.
    # --------------------------------------------------------------------------
    length = int(environ.get('CONTENT_LENGTH', '0'))
    logger.debug('TestControl Content Length: {0}'.format(length))
    body = environ['wsgi.input'].read(length)
    logger.debug('TestControl Content Body: {0}'.format(body))

    # --------------------------------------------------------------------------
    # If we have a schema file then check that the event matches that expected.
    # --------------------------------------------------------------------------
    if (schema is not None):
        logger.debug('Attempting to validate data: {0}\n'
                     'Against schema: {1}'.format(body, schema))
        try:
            decoded_body = json.loads(body)
            jsonschema.validate(decoded_body, schema)
            logger.info('TestControl is valid!')
            logger.info('TestControl:\n'
                        '{0}'.format(json.dumps(decoded_body,
                                                sort_keys=True,
                                                indent=4,
                                                separators=(',', ': '))))

        except jsonschema.SchemaError as e:
            logger.error('TestControl Schema is not valid: {0}'.format(e))

        except jsonschema.ValidationError as e:
            logger.warn('TestControl input not valid: {0}'.format(e))
            logger.warn('Bad JSON body decoded:\n'
                        '{0}'.format(json.dumps(decoded_body,
                                                sort_keys=True,
                                                indent=4,
                                                separators=(',', ': '))))

        except Exception as e:
            logger.error('TestControl input not valid: {0}'.format(e))
    else:
        logger.debug('Missing schema just decode JSON: {0}'.format(body))
        try:
            decoded_body = json.loads(body)
            logger.info('Valid JSON body (no schema checking) decoded:\n'
                        '{0}'.format(json.dumps(decoded_body,
                                                sort_keys=True,
                                                indent=4,
                                                separators=(',', ': '))))
            logger.info('TestControl input not checked against schema!')

        except Exception as e:
            logger.error('TestControl input not valid: {0}'.format(e))

    # --------------------------------------------------------------------------
    # Respond to the caller. If we received otherField 'ThrottleRequest',
    # generate the appropriate canned response.
    # --------------------------------------------------------------------------
    pending_command_list = decoded_body
    logger.info('===== TEST CONTROL END =====')
    logger.info('============================')
    start_response('202 Accepted', [])
    yield ''


def main(argv=None):
    '''
    Main function for the collector start-up.

    Called with command-line arguments:
        *    --config *<file>*
        *    --section *<section>*
        *    --verbose

    Where:

        *<file>* specifies the path to the configuration file.

        *<section>* specifies the section within that config file.

        *verbose* generates more information in the log files.

    The process listens for REST API invocations and checks them. Errors are
    displayed to stdout and logged.
    '''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = 'v{0}'.format(__version__)
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s {0} ({1})'.format(program_version,
                                                           program_build_date)
    if (__import__('__main__').__doc__ is not None):       # pragma: no cover
        program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
    else:
        program_shortdesc = 'Running in test harness'
    program_license = '''{0}

  Created  on {1}.
  Copyright 2015 Metaswitch Networks Ltd. All rights reserved.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
'''.format(program_shortdesc, str(__date__))

    try:
        # ----------------------------------------------------------------------
        # Setup argument parser so we can parse the command-line.
        # ----------------------------------------------------------------------
        parser = ArgumentParser(description=program_license,
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            action='count',
                            help='set verbosity level')
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message,
                            help='Display version information')
        parser.add_argument('-a', '--api-version',
                            dest='api_version',
                            default='7',
                            help='set API version')
        parser.add_argument('-c', '--config',
                            dest='config',
                            default='/etc/opt/att/collector.conf',
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
        verbose = args.verbose
        api_version = args.api_version
        config_file = args.config
        config_section = args.section
        assert (config_file != ""), "Config file is missing"

        # ----------------------------------------------------------------------
        # Now read the config file, using command-line supplied values as
        # overrides.
        # ----------------------------------------------------------------------
        overrides = {}
        config = configparser.ConfigParser()
        config['defaults'] = {'log_file': 'collector.log',
                              'vel_port': '12233',
                              'vel_path': '',
                              'vel_topic_name': ''
                              }
        config.read(config_file)

        # ----------------------------------------------------------------------
        # extract the values we want.
        # ----------------------------------------------------------------------
        global vel_username
        global vel_password
        global vel_topic_name
        global kafka_server
        global kafka_topic

        log_file = config.get(config_section, 'log_file', vars=overrides)
        vel_port = config.get(config_section, 'vel_port', vars=overrides)
        vel_path = config.get(config_section, 'vel_path', vars=overrides)
        kafka_server = config.get(config_section,
                              'kafka_server',
                              vars=overrides)
        kafka_topic = config.get(config_section,
                                         'kafka_topic',
                                         vars=overrides)
        vel_topic_name = config.get(config_section,
                                    'vel_topic_name',
                                    vars=overrides)
        vel_username = config.get(config_section,
                                  'vel_username',
                                  vars=overrides)
        vel_password = config.get(config_section,
                                  'vel_password',
                                  vars=overrides)
        vel_schema_file = config.get(config_section,
                                     'schema_file',
                                     vars=overrides)
        base_schema_file = config.get(config_section,
                                      'base_schema_file',
                                      vars=overrides)
        throttle_schema_file = config.get(config_section,
                                          'throttle_schema_file',
                                          vars=overrides)
        test_control_schema_file = config.get(config_section,
                                             'test_control_schema_file',
                                              vars=overrides)
        vel_yaml_schema = config.get(config_section,
                                     'yaml_schema_path',
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
            logger.setLevel(logging.INFO)
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


        assert (log_file != ""), "Value of property 'log_file' is missing in config file"
        assert (vel_schema_file != ""), "Value of property 'schema_file' is missing in config file"
        assert (kafka_server != ""), "Value of property 'kafka_server' is missing in config file"

        # ---------------------------------------------------------------------
        # Log the details of the configuration.
        # ---------------------------------------------------------------------
        logger.debug('Log file = {0}'.format(log_file))
        logger.debug('Event Listener Port = {0}'.format(vel_port))
        logger.debug('Event Listener Path = {0}'.format(vel_path))
        logger.debug('Event Listener Topic = {0}'.format(vel_topic_name))
        logger.debug('Event Listener Username = {0}'.format(vel_username))
        # logger.debug('Event Listener Password = {0}'.format(vel_password))
        logger.debug('Event Listener JSON Schema File = {0}'.format(
                                                              vel_schema_file))
        logger.debug('Base JSON Schema File = {0}'.format(base_schema_file))
        logger.debug('Throttle JSON Schema File = {0}'.format(
                                                         throttle_schema_file))
        logger.debug('Test Control JSON Schema File = {0}'.format(
                                                     test_control_schema_file))

        # ----------------------------------------------------------------------
        # Perform some basic error checking on the config.
        # ----------------------------------------------------------------------

        if (int(vel_port) < 1024 or int(vel_port) > 65535):
            logger.error('Invalid Vendor Event Listener port ({0}) '
                         'specified'.format(vel_port))
            raise RuntimeError('Invalid Vendor Event Listener port ({0}) '
                               'specified'.format(vel_port))

        if (len(vel_path) > 0 and vel_path[-1] != '/'):
            logger.warning('Event Listener Path ({0}) should have terminating '
                           '"/"!  Adding one on to configured string.'.format(
                                                                     vel_path))
            vel_path += '/'

        # ----------------------------------------------------------------------
        # Load up the vel_schema, if it exists.
        # ----------------------------------------------------------------------
        if not os.path.exists(vel_schema_file):
            logger.warning('Event Listener Schema File ({0}) not found. '
                           'No validation will be undertaken.'.format(
                                                              vel_schema_file))
        else:
            global vel_schema
            global throttle_schema
            global test_control_schema
            vel_schema = json.load(open(vel_schema_file, 'r'))
            logger.debug('Loaded the JSON schema file')

            # ------------------------------------------------------------------
            # Load up the throttle_schema, if it exists.
            # ------------------------------------------------------------------
            if (os.path.exists(throttle_schema_file)):
                logger.debug('Loading throttle schema')
                throttle_fragment = json.load(open(throttle_schema_file, 'r'))
                throttle_schema = {}
                throttle_schema.update(vel_schema)
                throttle_schema.update(throttle_fragment)
                logger.debug('Loaded the throttle schema')

            # ------------------------------------------------------------------
            # Load up the test control _schema, if it exists.
            # ------------------------------------------------------------------
            if (os.path.exists(test_control_schema_file)):
                logger.debug('Loading test control schema')
                test_control_fragment = json.load(
                    open(test_control_schema_file, 'r'))
                test_control_schema = {}
                test_control_schema.update(vel_schema)
                test_control_schema.update(test_control_fragment)
                logger.debug('Loaded the test control schema')

            # ------------------------------------------------------------------
            # Load up the base_schema, if it exists.
            # ------------------------------------------------------------------
            if (os.path.exists(base_schema_file)):
                logger.debug('Updating the schema with base definition')
                base_schema = json.load(open(base_schema_file, 'r'))
                vel_schema.update(base_schema)
                logger.debug('Updated the JSON schema file')

        # ----------------------------------------------------------------------
        # We are now ready to get started with processing. Start-up the various
        # components of the system in order:
        #
        #  1) Create the dispatcher.
        #  2) Register the functions for the URLs of interest.
        #  3) Run the webserver.
        # ----------------------------------------------------------------------
        root_url = '/{0}eventListener/v{1}{2}'.\
                   format(vel_path,
                          api_version,
                          '/' + vel_topic_name
                          if len(vel_topic_name) > 0
                          else '')
        throttle_url = '/{0}eventListener/v{1}/clientThrottlingState'.\
                       format(vel_path, api_version)
        set_404_content(root_url)
        global get_info
        get_info = root_url
        dispatcher = PathDispatcher()
        vendor_event_listener = partial(listener, schema=vel_schema, yaml_schema=vel_yaml_schema)
        dispatcher.register('GET', root_url, vendor_event_listener)
        dispatcher.register('POST', root_url, vendor_event_listener)
        vendor_throttle_listener = partial(listener, schema=throttle_schema)
        dispatcher.register('GET', throttle_url, vendor_throttle_listener)
        dispatcher.register('POST', throttle_url, vendor_throttle_listener)

        # ----------------------------------------------------------------------
        # We also add a POST-only mechanism for test control, so that we can
        # send commands to a single attached client.
        # ----------------------------------------------------------------------
        test_control_url = '/testControl/v{0}/commandList'.format(api_version)
        test_control_listener = partial(test_listener,
                                        schema=test_control_schema)
        dispatcher.register('POST', test_control_url, test_control_listener)
        dispatcher.register('GET', test_control_url, test_control_listener)

        httpd = pywsgi.WSGIServer(('', int(vel_port)), vendor_event_listener, keyfile='/opt/smo/certs/vescertificate.key', certfile='/opt/smo/certs/vescertificate.crt')
        logger.info('Serving on port {0}...'.format(vel_port))
        httpd.serve_forever()

        logger.error('Main loop exited unexpectedly!')
        return 0

    except KeyboardInterrupt:       # pragma: no cover
        # ----------------------------------------------------------------------
        # handle keyboard interrupt
        # ----------------------------------------------------------------------
        logger.info('Exiting on keyboard interrupt!')
        return 0

    except Exception as e:
        # ----------------------------------------------------------------------
        # Handle unexpected exceptions.
        # ----------------------------------------------------------------------
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help\n')
        sys.stderr.write(traceback.format_exc())
        logger.critical('Exiting because of exception: {0}'.format(e))
        logger.critical(traceback.format_exc())
        return 2

# ------------------------------------------------------------------------------
# MAIN SCRIPT ENTRY POINT.
# ------------------------------------------------------------------------------


if __name__ == '__main__':      # pragma: no cover
    if TESTRUN:
        # ----------------------------------------------------------------------
        # Running tests - note that doctest comments haven't been included so
        # this is a hook for future improvements.
        # ----------------------------------------------------------------------
        import doctest
        doctest.testmod()

    if PROFILE:
        # ----------------------------------------------------------------------
        # Profiling performance.  Performance isn't expected to be a major
        # issue, but this should all work as expected.
        # ----------------------------------------------------------------------
        import cProfile
        import pstats
        profile_filename = 'collector_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('collector_profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    # --------------------------------------------------------------------------
    # Normal operation - call through to the main function.
    # --------------------------------------------------------------------------
    sys.exit(main())

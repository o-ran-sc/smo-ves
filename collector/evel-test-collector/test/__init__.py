import os
import sys
import configparser

PROJECT_PATH = os.getcwd()
configfile_name = PROJECT_PATH+'/test_collector.conf'
PROJECT_PATH = PROJECT_PATH[:PROJECT_PATH.rfind('/')]
schema_file_path = os.path.join(
    PROJECT_PATH,"docs/att_interface_definition/CommonEventFormat-v7-2-2.json")
if  os.path.isfile(configfile_name):
    # Create the configuration file as it doesn't exist yet
    cfgfile = open(configfile_name, "w")
    # Add content to the file
    Config = configparser.ConfigParser()
    Config.add_section("default")
    Config.set('default','schema_file', schema_file_path)
    Config.set('default','base_schema_file', '/evel-test-collector/docs/att_interface_definition/base_schema.json')
    Config.set('default','throttle_schema_file', 'evel-test-collector/docs/att_interface_definition/throttle_schema.json')
    Config.set('default','test_control_schema_file', 'evel-test-collector/docs/att_interface_definition/test_control_schema.json')
    Config.set('default','log_file', 'collector.log')
    Config.set('default','vel_domain', '127.0.0.1')
    Config.set('default','vel_port', '9999')
    Config.set('default','vel_path', '')
    Config.set('default','vel_username', '')
    Config.set('default','vel_password', '')
    Config.set('default','vel_topic_name', '')
    Config.set('default','kafka_server', 'kafka-server')
    Config.set('default','kafka_topic', '')
    Config.write(cfgfile)
    cfgfile.close()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"code/collector"
)
sys.path.append(SOURCE_PATH)

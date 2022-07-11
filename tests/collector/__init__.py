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
## Copyright 2021 Xoriant Corporation
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
## Copyright 2021 Xoriant Corporation
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

import os
import sys
import configparser

PROJECT_PATH = os.getcwd()
configfile_name = PROJECT_PATH+'ves/tests/test_collector/test_collector.conf'
PROJECT_PATH = PROJECT_PATH[:PROJECT_PATH.rfind('/')]
schema_file_path = os.path.join(
    PROJECT_PATH,"ves/collector/evel-test-collector/docs/att_interface_definition/CommonEventFormat-v7-2-2.json")
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
    PROJECT_PATH,"ves/collector/evel-test-collector/code/collector")
print(SOURCE_PATH, PROJECT_PATH,schema_file_path)
sys.path.append(SOURCE_PATH)

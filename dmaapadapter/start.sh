#!/bin/bash
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

cd /opt/smo
touch dmaap.log

config_file="adapter/config/adapter.conf"

sed -i -- "s/kafka_broker =/kafka_broker = $kafka_host:$kafka_port/g" \
  $config_file
sed -i -- "s/log_level =/log_level = $log_level/g" \
  $config_file
sed -i -- "s/enable_assert =/enable_assert = $enable_assert/g" \
  $config_file


echo; echo $config_file
cat $config_file


if [ "$log_level" != "" ]; then
  if [ "$enable_assert" != "True" ]; then
    python3 -O /opt/smo/adapter/code/dmaap_adapter.py \
      --config /opt/smo/adapter/config/adapter.conf \
      --section default > /opt/smo/dmaap.log 2>&1
  else
    python3 /opt/smo/adapter/code/dmaap_adapter.py \
      --config /opt/smo/adapter/config/adapter.conf \
      --section default > /opt/smo/dmaap.log 2>&1
  fi
else
  if [ "$enable_assert" != "True" ]; then
    python3 -O /opt/smo/adapter/code/dmaap_adapter.py \
      --config /opt/smo/adapter/config/adapter.conf \
      --section default
   else
     python3 /opt/smo/adapter/code/dmaap_adapter.py \
       --config /opt/smo/adapter/config/adapter.conf \
       --section default
   fi
fi

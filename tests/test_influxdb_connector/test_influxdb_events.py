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

import configparser
import json
import logging
import os
import pytest
import sys
import influxdb_connector
from unittest import mock
from pathlib import Path
from unittest.mock import patch
from mock import MagicMock


def getEvent(arg):
    path = Path(__file__).parent
    fname = path /'events.txt'
    
    event_dictionary = {}
    with fname.open() as file:
        for line in file:
            key, value = line.split("=")
            event_dictionary[key] = value
            if key == arg:
               return value  
    return 'NA'


@pytest.fixture
def event_Timestamp():
    eventTimestamp = '1639985333218840'
    return eventTimestamp

# ------------------------------------------------------------------------------
# Address of heart_beat event unit test_case
# ------------------------------------------------------------------------------

@pytest.fixture
def hb_json():
            hb_jsonObj = {'additionalFields': {'eventTime': '2021-12-20T07:29:34.292938Z'}, 'heartbeatFieldsVersion': '3.0',
                    'heartbeatInterval': 20}
            return hb_jsonObj


@pytest.fixture
def hb_data():
            data = 'heartbeat,domain=heartbeat,eventId=ORAN-DEV_2021-12-20T07:29:34.292938Z,eventName=heartbeat_O_RAN_COMPONENT,eventType=O_RAN_COMPONENT,nfNamingCode=SDN-Controller,nfVendorName=O-RAN-SC-OAM,priority=Low,reportingEntityName=ORAN-DEV,sourceName=ORAN-DEV,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1'
            return data


@pytest.fixture
def hb_nonstringpdata():
            nonstringpdata = ' lastEpochMicrosec=1639965574292938,sequence=357,startEpochMicrosec=1639965574292938,'
            return nonstringpdata


@pytest.fixture
def hb_expected_pdata():
            heartbeat_expected_pdata = 'heartbeat,domain=heartbeat,eventId=ORAN-DEV_2021-12-20T07:29:34.292938Z,eventName=heartbeat_O_RAN_COMPONENT,eventType=O_RAN_COMPONENT,nfNamingCode=SDN-Controller,nfVendorName=O-RAN-SC-OAM,priority=Low,reportingEntityName=ORAN-DEV,sourceName=ORAN-DEV,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1,system=None,eventTime=2021-12-20T07:29:34.292938Z,heartbeatFieldsVersion=3.0 lastEpochMicrosec=1639965574292938,sequence=357,startEpochMicrosec=1639965574292938,heartbeatInterval=20 1639985333218840000'
            return heartbeat_expected_pdata


@mock.patch('influxdb_connector.send_to_influxdb') 
@mock.patch('influxdb_connector.process_time', return_value='1639985333218840000') 
def test_process_heartbeat_events_called(mocker_process_time, mocker_send_to_influxdb, hb_json, hb_data, hb_nonstringpdata, hb_expected_pdata, event_Timestamp):
    domain = "heartbeat"
    influxdb_connector.process_heartbeat_events(domain, hb_json, hb_data, hb_nonstringpdata)
    mocker_send_to_influxdb.assert_called_with(domain, hb_expected_pdata)
 
         
# ------------------------------------------------------------------------------
# Address of pnfRegistration event.
# ------------------------------------------------------------------------------

@pytest.fixture
def pnf_json():
            jobj = {'pnfRegistrationFieldsVersion': '2.1', 'lastServiceDate': '2021-03-26', 'macAddress': '02:42:f7:d4:62:ce', 'manufactureDate': '2021-01-16', 'modelNumber': 'ONAP Controller for Radio', 'oamV4IpAddress': '127.0.0.1', 'oamV6IpAddress': '0:0:0:0:0:ffff:a0a:0.1', 'serialNumber': 'ONAP-SDNR-127.0.0.1-ONAP Controller for Radio', 'softwareVersion': '2.3.5', 'unitFamily': 'ONAP-SDNR', 'unitType': 'SDNR', 'vendorName': 'ONAP', 'additionalFields': {'oamPort': '830', 'protocol': 'SSH', 'username': 'netconf', 'password': 'netconf', 'reconnectOnChangedSchema': 'false', 'sleep-factor': '1.5', 'tcpOnly': 'false', 'connectionTimeout': '20000', 'maxConnectionAttempts': '100', 'betweenAttemptsTimeout': '2000', 'keepaliveDelay': '120'}}
            return jobj


@pytest.fixture
def pnf_data():
            data = 'pnfRegistration,domain=pnfRegistration,eventId=ORAN-DEV_ONAP\\ Controller\\ for\\ Radio,eventName=pnfRegistration_EventType5G,eventType=EventType5G,priority=Low,reportingEntityName=ORAN-DEV,sourceName=ORAN-DEV,nfNamingCode=SDNR,nfVendorName=ONAP,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1'
            return data


@pytest.fixture
def pnf_nonstringpdata():
            nonstringpdata = ' sequence=0,startEpochMicrosec=1639985329569087,lastEpochMicrosec=1639985329569087,'
            return nonstringpdata


@pytest.fixture
def pnf_expected_pdata():
            pnf_expected_pdata = 'pnfRegistration,domain=pnfRegistration,eventId=ORAN-DEV_ONAP\\ Controller\\ for\\ Radio,eventName=pnfRegistration_EventType5G,eventType=EventType5G,priority=Low,reportingEntityName=ORAN-DEV,sourceName=ORAN-DEV,nfNamingCode=SDNR,nfVendorName=ONAP,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1,system=None,pnfRegistrationFieldsVersion=2.1,lastServiceDate=2021-03-26,macAddress=02:42:f7:d4:62:ce,manufactureDate=2021-01-16,modelNumber=ONAP\\ Controller\\ for\\ Radio,oamV4IpAddress=127.0.0.1,oamV6IpAddress=0:0:0:0:0:ffff:a0a:0.1,serialNumber=ONAP-SDNR-127.0.0.1-ONAP\\ Controller\\ for\\ Radio,softwareVersion=2.3.5,unitFamily=ONAP-SDNR,unitType=SDNR,vendorName=ONAP,oamPort=830,protocol=SSH,username=netconf,password=netconf,reconnectOnChangedSchema=false,sleep-factor=1.5,tcpOnly=false,connectionTimeout=20000,maxConnectionAttempts=100,betweenAttemptsTimeout=2000,keepaliveDelay=120 sequence=0,startEpochMicrosec=1639985329569087,lastEpochMicrosec=1639985329569087 1639985333218840000'
            return pnf_expected_pdata


@mock.patch('influxdb_connector.send_to_influxdb') 
@mock.patch('influxdb_connector.process_time', return_value='1639985333218840000') 
def test_process_pnfRegistration_event_called(mock_process_time ,mocker_send_to_influxdb, pnf_json, pnf_data, pnf_nonstringpdata, pnf_expected_pdata, event_Timestamp):
    domain = "pnfRegistration"
    
    influxdb_connector.process_pnfRegistration_event(domain, pnf_json, pnf_data, pnf_nonstringpdata)
    mocker_send_to_influxdb.assert_called_with(domain, pnf_expected_pdata)
         
         
# ------------------------------------------------------------------------------
# Address of fault event unit test case
# ------------------------------------------------------------------------------

@pytest.fixture
def flt_json():
            jobj = {'faultFieldsVersion': '1.0', 'alarmCondition': 'TCA', 'alarmInterfaceA': 'LP-MWPS-RADIO',
                     'eventSourceType': 'O_RAN_COMPONENT', 'specificProblem': 'TCA', 'eventSeverity': 'NORMAL',
                     'vfStatus': 'Active', 'alarmAdditionalInformation': {'eventTime': '2021-12-20T07:28:53.218840Z', 'equipType': 'FYNG', 'vendor': 'VENDORA', 'model': 'FancyNextGeneration'}}
            return jobj


@pytest.fixture
def flt_data():
            data = 'fault,domain=fault,eventId=LKCYFL79Q01M01FYNG01_LP-MWPS-RADIO_TCA,eventName=fault_O_RAN_COMPONENT_Alarms_TCA,eventType=O_RAN_COMPONENT_Alarms,priority=High,reportingEntityName=ORAN-DEV,sourceName=LKCYFL79Q01M01FYNG01,nfNamingCode=FYNG,nfVendorName=VENDORA,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1'
            return data


@pytest.fixture
def flt_nonstringpdata():
            nonstringpdata = ' sequence=0,startEpochMicrosec=1639985333218840,lastEpochMicrosec=1639985333218840,'
            return nonstringpdata


@pytest.fixture
def flt_expected_pdata():
            expected_pdata = 'fault,domain=fault,eventId=LKCYFL79Q01M01FYNG01_LP-MWPS-RADIO_TCA,eventName=fault_O_RAN_COMPONENT_Alarms_TCA,eventType=O_RAN_COMPONENT_Alarms,priority=High,reportingEntityName=ORAN-DEV,sourceName=LKCYFL79Q01M01FYNG01,nfNamingCode=FYNG,nfVendorName=VENDORA,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1,system=None,faultFieldsVersion=1.0,alarmCondition=TCA,alarmInterfaceA=LP-MWPS-RADIO,eventSourceType=O_RAN_COMPONENT,specificProblem=TCA,eventSeverity=NORMAL,vfStatus=Active,eventTime=2021-12-20T07:28:53.218840Z,equipType=FYNG,vendor=VENDORA,model=FancyNextGeneration sequence=0,startEpochMicrosec=1639985333218840,lastEpochMicrosec=1639985333218840 1639985333218840000'
            return expected_pdata


@mock.patch('influxdb_connector.send_to_influxdb') 
@mock.patch('influxdb_connector.process_time', return_value='1639985333218840000') 
def test_process_fault_event_called(mock_time,mocker_send_to_influxdb, flt_json, flt_data, flt_nonstringpdata, flt_expected_pdata, event_Timestamp):
    domain = "fault"
    
    influxdb_connector.process_fault_event(domain, flt_json, flt_data, flt_nonstringpdata)
    mocker_send_to_influxdb.assert_called_with(domain, flt_expected_pdata)
       
         
# ------------------------------------------------------------------------------
# Address of measurement event unit test_cases
# ------------------------------------------------------------------------------

@pytest.fixture
def event_Id():
    eventId = "O-RAN-FH-IPv6-01_1639984500_PM15min"
    return eventId


@pytest.fixture
def start_Epoch_Microsec():
    startEpochMicrosec = "1639983600000"
    return startEpochMicrosec


@pytest.fixture
def last_Epoch_Microsec():
    lastEpochMicrosec = "1639984500000"
    return lastEpochMicrosec

@pytest.fixture
def meas_json():
            jobj = {'additionalFields': {}, 'additionalMeasurements': [{'name': 'LP-MWPS-RADIO-1', 'hashMap': {'es': 
                     '0', 'ses': '1', 'cses': '0', 'unavailability': '0'}}, {'name': 'LP-MWPS-RADIO-2', 'hashMap': {'es': '0', 'ses': '1',
                     'cses': '0', 'unavailability': '0'}}], 'additionalObjects': [], 'codecUsageArray': [], 'concurrentSessions': 2,
                     'configuredEntities': 2, 'cpuUsageArray': [], 'diskUsageArray': [], 'featureUsageArray': {'https://www.itu.int/rec/T-REC-G.841': 'true'}, 'filesystemUsageArray': [], 'hugePagesArray': [], 'ipmi': {},
                     'latencyDistribution': [], 'loadArray': [], 'machineCheckExceptionArray': [], 'meanRequestLatency': 1000,
                     'measurementInterval': 234, 'measurementFieldsVersion': '4.0', 'memoryUsageArray': [],
                     'numberOfMediaPortsInUse': 234, 'requestRate': 23, 'nfcScalingMetric': 3, 'nicPerformanceArray': [],
                     'processStatsArray': []}
            return jobj

@pytest.fixture
def meas_data():
            data = 'measurement,domain=measurement,eventId=O-RAN-FH-IPv6-01_1639984500_PM15min,eventName=measurement_O_RAN_COMPONENT_PM15min,eventType=O_RAN_COMPONENT_PM15min,priority=Low,reportingEntityName=ORAN-DEV,sourceName=O-RAN-FH-IPv6-01,intervalStartTime=Mon\,\ 20\ Dec\ 2021\ 07:00:00\ +0000,intervalEndTime=Mon\,\ 20\ Dec\ 2021\ 07:15:00\ +0000,version=4.1,vesEventListenerVersion=7.2.1'
            return data

@pytest.fixture
def meas_nonstringpdata():
            nonstringpdata = ' sequence=0,startEpochMicrosec=1639983600000,lastEpochMicrosec=1639984500000,'
            return nonstringpdata


@pytest.fixture
def add_meas_data():
    data_set = {'additionalMeasurements': [{'name': 'LP-MWPS-RADIO-1', 'hashMap': {'es': 
                 '0', 'ses': '1', 'cses': '0', 'unavailability': '0'}}, {'name': 'LP-MWPS-RADIO-2', 'hashMap': {'es': '0', 'ses': '1',
                 'cses': '0', 'unavailability': '0'}}]}
    return data_set

@pytest.fixture
def non_add_meas_data():
    data_set = {'measurementcpuusage': [{'name': 'LP-MWPS-RADIO-1', 'hashMap': {'es': 
                 '0', 'ses': '1', 'cses': '0', 'unavailability': '0'}}, {'name': 'LP-MWPS-RADIO-2', 'hashMap': {'es': '0', 'ses': '1',
                 'cses': '0', 'unavailability': '0'}}]}
    return data_set

@pytest.fixture
def meas_expected_data():
            measurement_expected_pdata = 'measurement,domain=measurement,eventId=O-RAN-FH-IPv6-01_1639984500_PM15min,eventName=measurement_O_RAN_COMPONENT_PM15min,eventType=O_RAN_COMPONENT_PM15min,priority=Low,reportingEntityName=ORAN-DEV,sourceName=O-RAN-FH-IPv6-01,intervalStartTime=Mon\\,\\ 20\\ Dec\\ 2021\\ 07:00:00\\ +0000,intervalEndTime=Mon\\,\\ 20\\ Dec\\ 2021\\ 07:15:00\\ +0000,version=4.1,vesEventListenerVersion=7.2.1,system=None,https://www.itu.int/rec/T-REC-G.841=true,measurementFieldsVersion=4.0 sequence=0,startEpochMicrosec=1639983600000,lastEpochMicrosec=1639984500000,concurrentSessions=2,configuredEntities=2,meanRequestLatency=1000,measurementInterval=234,numberOfMediaPortsInUse=234,requestRate=23,nfcScalingMetric=3 1639985333218840000'
            return measurement_expected_pdata

        
# ## process_measurement_events unit test_cases.
@patch('influxdb_connector.process_nonadditional_measurements')
@patch('influxdb_connector.process_additional_measurements')
@patch('influxdb_connector.send_to_influxdb')
@mock.patch('influxdb_connector.process_time', return_value='1639985333218840000') 
def test_process_measurement_events_called(mock_time,mocker_send_to_influxdb, mocker_additional, mocker_nonadditional, meas_json,
                                           meas_data, meas_nonstringpdata, event_Id, start_Epoch_Microsec, last_Epoch_Microsec,
                                           meas_expected_data, non_add_meas_data, add_meas_data, event_Timestamp):
    domain = "measurement"
    
    influxdb_connector.process_measurement_events('measurement', meas_json, meas_data, meas_nonstringpdata, event_Id,
                                                  start_Epoch_Microsec, last_Epoch_Microsec)
    mocker_additional.process_additional_measurements(add_meas_data.get('additionalMeasurements'), 'measurementadditionalmeasurements',
                                                      event_Id, start_Epoch_Microsec, last_Epoch_Microsec)
    mocker_additional.assert_called_with(add_meas_data.get('additionalMeasurements'), 'measurementadditionalmeasurements', event_Id,
                                         start_Epoch_Microsec, last_Epoch_Microsec)
    
    mocker_nonadditional.process_nonadditional_measurements([], 'measurementnicperformance', event_Id, start_Epoch_Microsec, last_Epoch_Microsec)
    mocker_nonadditional.assert_called_with([], 'measurementnicperformance', event_Id, start_Epoch_Microsec, last_Epoch_Microsec)
    mocker_send_to_influxdb.assert_called_with(domain, meas_expected_data)


@pytest.fixture
def add_meas_expected_pdata():
            additional_expected_pdata = 'measurementadditionalmeasurements,eventId=O-RAN-FH-IPv6-01_1639984500_PM15min,system=None,name=LP-MWPS-RADIO-2,es=0,ses=1,cses=0,unavailability=0 startEpochMicrosec=1639983600000,lastEpochMicrosec=1639984500000 1639985333218840000'
            return additional_expected_pdata


# ## process_additional_measurements unit test_case
@mock.patch('influxdb_connector.send_to_influxdb')
@mock.patch('influxdb_connector.process_time', return_value='1639985333218840000') 
def test_process_additional_measurements_called(mock_time, mocker_send_to_influxdb, event_Id, start_Epoch_Microsec, last_Epoch_Microsec, 
                                                add_meas_data, add_meas_expected_pdata, event_Timestamp):
    payload = add_meas_data
    domain = 'measurementadditionalmeasurements'
    for key, val in payload.items():
            if isinstance(val, list):
                if key == 'additionalMeasurements':
                    influxdb_connector.process_additional_measurements(payload.get('additionalMeasurements'), domain, 
                                                                       event_Id, start_Epoch_Microsec, last_Epoch_Microsec)
                    mocker_send_to_influxdb.assert_called_with(domain, add_meas_expected_pdata)


@pytest.fixture
def non_add_expected_data():
            non_additional_expected_pdata = "measurementcpuusage,eventId=O-RAN-FH-IPv6-01_1639984500_PM15min,system=None,name=LP-MWPS-RADIO-2 startEpochMicrosec=1639983600000,lastEpochMicrosec=1639984500000,hashMap={'es': '0', 'ses': '1', 'cses': '0', 'unavailability': '0'} 1639985333218840000"
            return non_additional_expected_pdata


# ## process_nonadditional_measurements unit test_cases.
@mock.patch('influxdb_connector.send_to_influxdb')
@mock.patch('influxdb_connector.process_time', return_value='1639985333218840000') 
def test_process_nonadditional_measurements_called(mock_time, mocker_send_to_influxdb, event_Id, start_Epoch_Microsec, 
                                                   last_Epoch_Microsec, non_add_meas_data, non_add_expected_data, event_Timestamp):
    domain = 'measurementcpuusage'
    source = 'unkown'
    
    influxdb_connector.process_nonadditional_measurements(non_add_meas_data.get('measurementcpuusage'), domain, event_Id, 
                                                          start_Epoch_Microsec, last_Epoch_Microsec)
    mocker_send_to_influxdb.assert_called_with(domain, non_add_expected_data)


# ------------------------------------------------------------------------------
# Address of threshold event unit test_case
# ------------------------------------------------------------------------------

@pytest.fixture
def thre_json():
            jobj = {'thresholdCrossingFieldsVersion': '4.0', 'additionalParameters': [{'criticality': 'MAJ', 'hashMap': 
                     {'additionalProperties': 'up-and-down'}, 'thresholdCrossed': 'packetLoss'}], 'alertAction': 'SET',
                     'alertDescription': 'TCA', 'alertType': 'INTERFACE-ANOMALY', 'alertValue': '1OSF',
                     'associatedAlertIdList': ['loss-of-signal'], 'collectionTimestamp': 'Mon, 20 Dec 2021 07:28:56 +0000',
                     'dataCollector': 'data-lake', 'elementType': '1OSF', 'eventSeverity': 'WARNING', 'eventStartTimestamp': 
                     'Mon, 20 Dec 2021 07:15:00 +0000', 'interfaceName': '', 'networkService': 'from-a-to-b',
                     'possibleRootCause': 'always-the-others', 'additionalFields': {'eventTime': '2021-12-20T07:28:56.443218Z',
                     'equipType': '1OSF', 'vendor': '', 'model': ''}}
            return jobj


@pytest.fixture
def threshold_data():
            data = 'thresholdCrossingAlert,domain=thresholdCrossingAlert,eventId=__TCA,eventName=thresholdCrossingAlert_O_RAN_COMPONENT_TCA_TCA,eventType=O_RAN_COMPONENT_TCA,priority=High,reportingEntityName=ORAN-DEV,nfNamingCode=1OSF,timeZoneOffset=+00:00,version=4.1,vesEventListenerVersion=7.2.1'
            return str(data)


@pytest.fixture
def thres_nonstringpdata():
            nonstringpdata = ' sequence=0,startEpochMicrosec=1639985336443218,lastEpochMicrosec=1639985336443218,'
            return str(nonstringpdata)



def test_process_thresholdCrossingAlert_event_called(thre_json, threshold_data, thres_nonstringpdata, event_Timestamp):
    domain = "thresholdCrossingAlert"
    
    with patch('influxdb_connector.process_thresholdCrossingAlert_event') as func:
         influxdb_connector.process_thresholdCrossingAlert_event(domain, thre_json, threshold_data, thres_nonstringpdata)
         func.assert_called_with(domain, thre_json, threshold_data, thres_nonstringpdata)


# ## save_event_in_db unit test_cases.
@patch('influxdb_connector.logger')
@pytest.mark.parametrize("key", [("heartbeat"), ("pnfRegistration"), ("measurement"), ("fault"), ("thresholdCrossingAlert")])
def test_save_event_in_db(mock_logger, key, hb_json, hb_data, hb_nonstringpdata, pnf_json, pnf_data, pnf_nonstringpdata,
                                         meas_json, meas_data, meas_nonstringpdata, event_Id, start_Epoch_Microsec, last_Epoch_Microsec,
                                         flt_json, flt_data, flt_nonstringpdata,
                                         thre_json, threshold_data, thres_nonstringpdata):
    
    if(key == 'heartbeat'):
        data_set = getEvent("heartbeat")
        with patch('influxdb_connector.process_heartbeat_events') as func:
             influxdb_connector.save_event_in_db(data_set)
             func.assert_called_with('heartbeat', hb_json, hb_data, hb_nonstringpdata)
    
    elif(key == 'pnfRegistration'):
          data_set = getEvent("pnfRegistration")
          with patch('influxdb_connector.process_pnfRegistration_event') as func:
             influxdb_connector.save_event_in_db(data_set)      
             func.assert_called_with('pnfRegistration', pnf_json, pnf_data, pnf_nonstringpdata)  
       
    elif(key == 'measurement'):
          data_set = getEvent("measurement")
          with patch('influxdb_connector.process_measurement_events') as func:
             influxdb_connector.save_event_in_db(data_set)      
             func.assert_called_with('measurement', meas_json, meas_data, meas_nonstringpdata, event_Id, int(start_Epoch_Microsec), 
                                     int(last_Epoch_Microsec))           
        
    elif(key == 'fault'):
          data_set = getEvent("fault")
          with patch('influxdb_connector.process_fault_event') as func:
             influxdb_connector.save_event_in_db(data_set)      
             func.assert_called_with('fault', flt_json, flt_data, flt_nonstringpdata)
      
    elif(key == 'thresholdCrossingAlert'):
          data_set = getEvent("thresholdCrossingAlert")
          with patch('influxdb_connector.process_thresholdCrossingAlert_event') as func:
               influxdb_connector.save_event_in_db(data_set)
               func.assert_called_with('thresholdCrossingAlert', thre_json, threshold_data, thres_nonstringpdata)
   

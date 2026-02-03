#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

from aria.ops.event import Criticality
from constants.main import DELL_EMC_SERVER_PREFIX

def collect_event_data(host_obj, event):
    # Push events Created
    message = f'{DELL_EMC_SERVER_PREFIX}[Date] {event["Created"]} | [Fault] {event["Message"]} | [Part] {event["Name"]} | [Sensor] {event["SensorType"]}'
    #if event["Severity"] == "OK":
    #    host_obj.with_event(message = message, criticality=Criticality.INFO)
    if event["Severity"] == "Warning":
        host_obj.with_event(message = message, criticality=Criticality.WARNING)
    if event["Severity"] == "Critical":
        host_obj.with_event(message = message, criticality=Criticality.CRITICAL)
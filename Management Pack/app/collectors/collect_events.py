#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

from aria.ops.event import Criticality

def collect_event_data(host_obj, event):
    # Push events
    message = f'[Fault] {event["Message"]} | [Part] {event["Name"]} | [Sensor] {event["SensorType"]}'
    host_obj.with_event(message = message, criticality=Criticality.CRITICAL)
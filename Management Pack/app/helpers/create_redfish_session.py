#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import requests
from aria.ops.event import Criticality
from constants.main import DELL_EMC_SERVER_PREFIX

def create_redfish_session(server, username, password, physicalServerConfigFile_obj):
    url = f"{server}/redfish/v1/SessionService/Sessions"
    headers = {"Content-Type": "application/json"}
    payload = {"UserName": username, "Password": password}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code in [200, 201]:
        token = response.headers.get("X-Auth-Token")
        session_uri = response.headers.get("Location")
        return token, session_uri
    else:
        message = f'{DELL_EMC_SERVER_PREFIX}Redfish session failed for {server}. Check your credentials. Response Code: {response.status_code}'
        physicalServerConfigFile_obj.with_event(message = message, criticality=Criticality.WARNING)
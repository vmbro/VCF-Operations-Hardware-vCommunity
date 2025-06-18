#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import requests
from constants.system_api_constants import SYSTEM_API_KEYS
from collectors.collect_redfish_info import collect_redfish_data
from collectors.collect_fan_info import collect_fan_data
from collectors.collect_events import collect_event_data
from collectors.collect_disk_info import collect_controller_data
import aria.ops.adapter_logging as logging


logger = logging.getLogger("collect_main_data")

def collect_main_data(IDRAC_IP, USERNAME, PASSWORD, host_obj, datacenter):
    server = check_host(IDRAC_IP)
    #Get System API Info
    URL = f"{server}/redfish/v1/Systems/System.Embedded.1"
    response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
    if response.status_code == 200:
        data = response.json()
        host_obj.with_property("Summary|Parent Datacenter", datacenter)
        
        for key in SYSTEM_API_KEYS:
            group, value = get_grouped_value(data, key)
            host_obj.with_property(str(f"{group}|{key[0]}"), str(value))

        #Get Redfish API Info
        URL = f"{server}/redfish/v1/"
        response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
        if response.status_code == 200:
            redfishData = response.json()
            collect_redfish_data(host_obj, redfishData)

        #Get Thermal FAN API Info
        URL = f"{server}/redfish/v1/Chassis/System.Embedded.1/ThermalSubsystem/Fans"
        response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
        if response.status_code == 200:
            fanMembers = response.json()
            for fanMember in fanMembers["Members"]:
                fanPath = fanMember["@odata.id"]
                URL = f"{server}{fanPath}"
                response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
                if response.status_code == 200:
                    fan = response.json()
                    collect_fan_data(host_obj, fan)

        #Get events
        URL = f"{server}/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/FaultList/Entries"
        response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
        if response.status_code == 200:
            events = response.json()
            for event in events["Members"]:
                collect_event_data(host_obj, event)

        #Get Storage Controller Info
        URL = f"{server}/redfish/v1/Systems/System.Embedded.1/Storage"
        response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
        if response.status_code == 200:
            controllerMembers = response.json()
            controllers = controllerMembers.get("Members", [])

            for controller in controllers:
                controllerId = controller["@odata.id"]
                collect_controller_data(host_obj, controllerId, server, USERNAME, PASSWORD)




def check_host(server):
    if server.startswith("http"):
        return str(server)
    else:
        return f"https://{server}"


#def get_grouped_value(data, keys, default="N/A"):
#    value = data
#    for key in keys[1]:
#        if isinstance(value, list):
#            value = value[0] if value else default
#        elif isinstance(value, dict):
#            value = value.get(key, default)
#        else:
#            value = default
#    group = " | ".join(keys[2])
#    return group, value

def get_grouped_value(data, keys, default="null"):
    value = data
    for key in keys[1]:
        if isinstance(value, list):
            value = value[0] if value else default
        elif isinstance(value, dict):
            value = value.get(key, default)
        else:
            value = default

    if value is None:
        value = default
    group = " | ".join(keys[2])
    return group, value
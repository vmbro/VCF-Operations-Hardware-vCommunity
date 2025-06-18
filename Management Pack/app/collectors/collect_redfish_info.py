#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

def collect_redfish_data(host_obj, data):
    # Push Redfish API info
    host_obj.with_property("Summary|Redfish|ID", data["Id"])
    host_obj.with_property("Summary|Redfish|Manager MAC Address", data["Oem"]["Dell"]["ManagerMACAddress"])
    host_obj.with_property("Summary|Redfish|Service Tag", data["Oem"]["Dell"]["ServiceTag"])
    host_obj.with_property("Summary|Redfish|Product", data["Product"])
    host_obj.with_property("Summary|Redfish|Redfish Version", data["RedfishVersion"])
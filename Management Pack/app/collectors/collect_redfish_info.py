#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

UNKNOWN = "unknown"

def collect_redfish_data(physicalServer_obj, data):
    # Push Redfish API info
    #id = data["Id"]
    #managerMACAddress = data["Oem"]["Dell"]["ManagerMACAddress"]
    #product = data["Product"]
    #redfishVersion = data["RedfishVersion"]

    id = data.get("Id") or UNKNOWN
    managerMACAddress = data.get("Oem", {}).get("Dell", {}).get("ManagerMACAddress") or UNKNOWN
    product = data.get("Product") or UNKNOWN
    redfishVersion = data.get("RedfishVersion") or UNKNOWN

    physicalServer_obj.with_property("Summary|Redfish|ID", id)
    physicalServer_obj.with_property("Summary|Redfish|Manager MAC Address", managerMACAddress)
    physicalServer_obj.with_property("Summary|Redfish|Product", product)
    physicalServer_obj.with_property("Summary|Redfish|Redfish Version", redfishVersion)
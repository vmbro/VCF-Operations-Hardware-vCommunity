#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

NULL_STATUS = 0
UNKNOWN = "unknown"

def collect_os_data(host_obj, data):
    # Push OS API info
    #osName = data["Attributes"]["ServerOS.1.OSName"]
    #osVersion = data["Attributes"]["ServerOS.1.OSVersion"]
    #serverPoweredOnTime = data["Attributes"]["ServerOS.1.ServerPoweredOnTime"]
    #productKey = data["Attributes"]["ServerOS.1.ProductKey"]

    osName = data.get("Attributes", {}).get("ServerOS.1.OSName") or UNKNOWN
    osVersion = data.get("Attributes", {}).get("ServerOS.1.OSVersion") or UNKNOWN
    serverPoweredOnTime = data.get("Attributes", {}).get("ServerOS.1.ServerPoweredOnTime") or NULL_STATUS
    #productKey = data.get("Attributes", {}).get("ServerOS.1.ProductKey") or NULL_STATUS


    days = serverPoweredOnTime / (60 * 60 * 24)
    serverPoweredOnTime = int(days)

    #host_obj.with_property("Summary|Operating System|Product Key", productKey)
    host_obj.with_property("Summary|Operating System|Name", osName)
    host_obj.with_property("Summary|Operating System|Version", osVersion)
    host_obj.with_metric("Summary|Operating System|Powered on Time", serverPoweredOnTime)
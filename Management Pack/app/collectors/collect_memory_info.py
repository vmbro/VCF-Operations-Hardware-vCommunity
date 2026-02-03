#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

NULL_STATUS = 0
UNKNOWN = "unknown"

# collectors/collect_memory_info.py içinde
def collect_memory_data(physicalServer_obj, dimmData):
    name = dimmData.get("Name", {}) or UNKNOWN
    baseModuleType = dimmData.get("BaseModuleType", {}) or UNKNOWN
    capacityMiB = dimmData.get("CapacityMiB", {}) or UNKNOWN
    enabled = dimmData.get("Enabled", {}) or UNKNOWN
    errorCorrection = dimmData.get("ErrorCorrection", {}) or UNKNOWN
    manufacturer = dimmData.get("Manufacturer", {}) or UNKNOWN
    memoryDeviceType = dimmData.get("MemoryDeviceType", {}) or UNKNOWN
    memoryType = dimmData.get("MemoryType", {}) or UNKNOWN
    operatingSpeedMhz = dimmData.get("OperatingSpeedMhz", {}) or UNKNOWN
    partNumber = dimmData.get("PartNumber", {}) or UNKNOWN
    rankCount = dimmData.get("RankCount", {}) or UNKNOWN
    serialNumber = dimmData.get("SerialNumber", {}) or UNKNOWN
    memoryHealth = dimmData.get("Status", {}).get("Health") or UNKNOWN
    memoryState = dimmData.get("Status", {}).get("State") or UNKNOWN
    

    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Base Module Type", baseModuleType)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Capacity", capacityMiB)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Enabled", enabled)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Error Correction", errorCorrection)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Manufacturer", manufacturer)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Device Type", memoryDeviceType)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Type", memoryType)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Speed", operatingSpeedMhz)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Part Number", partNumber)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Rank Count", rankCount)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory Serial Number", serialNumber)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|DIMM Health", memoryHealth)
    physicalServer_obj.with_property(f"Hardware|Memory:{name}|Memory State", memoryState)
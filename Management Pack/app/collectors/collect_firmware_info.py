#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven
import logging

logger = logging.getLogger(__name__)

def collect_firmware_inventory_data(host_obj, firmwareInventory):
    # Push Firmware Inventory API Info
    firmwareName = firmwareInventory["Name"]
    firmwareVersion = firmwareInventory["Version"]

    host_obj.with_property(f"Firmware:{firmwareName}|Version", firmwareVersion)
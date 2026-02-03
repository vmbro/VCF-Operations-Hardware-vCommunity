#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import requests
from constants.system_api_constants import SYSTEM_API_KEYS
import aria.ops.adapter_logging as logging

logger = logging.getLogger(__name__)
NULL_STATUS = 0
UNKNOWN = "unknown"

def collect_volume_data(physicalServer_obj, controllerData, server, headers):
    # Push volume info
    
    volumesURL = controllerData["Volumes"]["@odata.id"]
    response = requests.get(f"{server}{volumesURL}", headers=headers, verify=False)
    if response.ok:
        volumesData = response.json()
        for volume in volumesData.get("Members", []):
            volumeId = volume["@odata.id"]
            if "Virtual" in volumeId.split("/Volumes/")[-1]:
                response = requests.get(f"{server}{volumeId}", headers=headers, verify=False)
                if response.ok:
                    volume = response.json()

                    #name = volume.get("Name") or NULL_STATUS
                    #blockSizeBytes = volume.get("BlockSizeBytes") or NULL_STATUS
                    #capacityBytes = volume.get("CapacityBytes") or NULL_STATUS
                    #busProtocol = volume.get("Oem", {}).get("Dell", {}).get("DellVolume", {}).get("BusProtocol") or NULL_STATUS
                    #mediaType = volume.get("Oem", {}).get("Dell", {}).get("DellVolume", {}).get("MediaType") or NULL_STATUS
                    #remainingRedundancy = volume["Oem"]["Dell"]["DellVolume"]["RemainingRedundancy"] or NULL_STATUS
                    #stripeSize = volume["Oem"]["Dell"]["DellVolume"]["StripeSize"] or NULL_STATUS
                    #RAIDType = volume["RAIDType"] or NULL_STATUS
                    #readCachePolicy = volume["ReadCachePolicy"] or NULL_STATUS
                    #health = volume["Status"]["Health"] or NULL_STATUS
                    #state = volume["Status"]["Health"] or NULL_STATUS
                    #volumeType = volume["VolumeType"] or NULL_STATUS

                    name = volume.get("Name") or UNKNOWN
                    blockSizeBytes = volume.get("BlockSizeBytes") or UNKNOWN
                    capacityBytes = volume.get("CapacityBytes") or UNKNOWN
                    busProtocol = volume.get("Oem", {}).get("Dell", {}).get("DellVolume", {}).get("BusProtocol") or UNKNOWN
                    mediaType = volume.get("Oem", {}).get("Dell", {}).get("DellVolume", {}).get("MediaType") or UNKNOWN
                    remainingRedundancy = volume.get("Oem", {}).get("Dell", {}).get("DellVolume", {}).get("RemainingRedundancy") or NULL_STATUS
                    stripeSize = volume.get("Oem", {}).get("Dell", {}).get("DellVolume", {}).get("StripeSize") or UNKNOWN
                    RAIDType = volume.get("RAIDType") or UNKNOWN
                    readCachePolicy = volume.get("ReadCachePolicy") or UNKNOWN
                    health = volume.get("Status", {}).get("Health") or UNKNOWN
                    state = volume.get("Status", {}).get("State") or UNKNOWN
                    volumeType = volume.get("VolumeType") or UNKNOWN


                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume Name", name)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume Block Size", blockSizeBytes)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume Capacity", capacityBytes)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Bus Protocol", busProtocol)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume Media Type", mediaType)
                    physicalServer_obj.with_metric(f"Hardware|Controller|Volumes:{name}|Remaining Redundancy", remainingRedundancy)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Stripe Size", stripeSize)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|RAID Type", RAIDType)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Read Cache Policy", readCachePolicy)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume Health", health)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume State", state)
                    physicalServer_obj.with_property(f"Hardware|Controller|Volumes:{name}|Volume Type", volumeType)



def collect_controller_data(physicalServer_obj, controllerData, server, headers):
    #Push Physical Disks info

    drives = controllerData.get("Drives", [])
    for drive in drives:
        driveId = drive["@odata.id"]
        url = f"{server}{driveId}"
        response = requests.get(url, headers=headers, verify=False)
        if response.ok:
            driveData = response.json()

            #name = driveData["Name"] or NULL_STATUS
            #blockSizeBytes = driveData["BlockSizeBytes"] or NULL_STATUS
            #capableSpeedGbs = driveData["CapableSpeedGbs"] or NULL_STATUS
            #capacityBytes = driveData["CapacityBytes"] or NULL_STATUS
            #encryptionStatus = driveData["EncryptionStatus"] or NULL_STATUS
            #hotspareType = driveData["HotspareType"] or NULL_STATUS
            #manufacturer = driveData["Manufacturer"] or NULL_STATUS
            #mediaType = driveData["MediaType"] or NULL_STATUS
            #model = driveData["Model"] or NULL_STATUS
            #negotiatedSpeedGbs = driveData["NegotiatedSpeedGbs"] or NULL_STATUS
            #cryptographicEraseCapable = driveData["Oem"]["Dell"]["DellPhysicalDisk"]["CryptographicEraseCapable"] or NULL_STATUS
            #driveFormFactor = driveData["Oem"]["Dell"]["DellPhysicalDisk"]["DriveFormFactor"] or NULL_STATUS
            #productID = driveData["Oem"]["Dell"]["DellPhysicalDisk"]["ProductID"] or NULL_STATUS
            #systemEraseCapability = driveData["Oem"]["Dell"]["DellPhysicalDisk"]["SystemEraseCapability"] or NULL_STATUS
            #partNumber = driveData["PartNumber"] or NULL_STATUS
            #predictedMediaLifeLeftPercent = driveData["PredictedMediaLifeLeftPercent"] or NULL_STATUS
            #protocol = driveData["Protocol"] or NULL_STATUS
            #revision = driveData["Revision"] or NULL_STATUS
            #serialNumber = driveData["SerialNumber"] or NULL_STATUS
            #driveHealth = driveData["Status"]["Health"] or NULL_STATUS

            name = driveData.get("Name") or UNKNOWN
            blockSizeBytes = driveData.get("BlockSizeBytes") or UNKNOWN
            capableSpeedGbs = driveData.get("CapableSpeedGbs") or UNKNOWN
            capacityBytes = driveData.get("CapacityBytes") or UNKNOWN
            encryptionStatus = driveData.get("EncryptionStatus") or UNKNOWN
            hotspareType = driveData.get("HotspareType") or UNKNOWN
            manufacturer = driveData.get("Manufacturer") or UNKNOWN
            mediaType = driveData.get("MediaType") or UNKNOWN
            model = driveData.get("Model") or UNKNOWN
            negotiatedSpeedGbs = driveData.get("NegotiatedSpeedGbs") or UNKNOWN
            cryptographicEraseCapable = driveData.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {}).get("CryptographicEraseCapable") or UNKNOWN
            driveFormFactor = driveData.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {}).get("DriveFormFactor") or UNKNOWN
            productID = driveData.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {}).get("ProductID") or UNKNOWN
            systemEraseCapability = driveData.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {}).get("SystemEraseCapability") or UNKNOWN
            partNumber = driveData.get("PartNumber") or UNKNOWN
            predictedMediaLifeLeftPercent = driveData.get("PredictedMediaLifeLeftPercent") or NULL_STATUS
            protocol = driveData.get("Protocol") or UNKNOWN
            revision = driveData.get("Revision") or UNKNOWN
            serialNumber = driveData.get("SerialNumber") or UNKNOWN
            driveHealth = driveData.get("Status", {}).get("Health") or UNKNOWN


            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Disk Name", name)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Disk Block Size", blockSizeBytes)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Capable Speed", capableSpeedGbs)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Disk Capacity", capacityBytes)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Encryption Status", encryptionStatus)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Hotspare Type", hotspareType)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Manufacturer", manufacturer)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Disk Media Type", mediaType)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Disk Model", model)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Negotiated Speed", negotiatedSpeedGbs)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Cryptographic Erase Capable", cryptographicEraseCapable)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Drive Form Factor", driveFormFactor)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Product ID", productID)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|System Erase Capability", systemEraseCapability)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Part Number", partNumber)
            physicalServer_obj.with_metric(f"Hardware|Controller|Physical Disks:{name}|Predicted Media Life Left Percent", predictedMediaLifeLeftPercent)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Protocol", protocol)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Revision", revision)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Drive Serial Number", serialNumber)
            physicalServer_obj.with_property(f"Hardware|Controller|Physical Disks:{name}|Drive Health", driveHealth)


    collect_volume_data(physicalServer_obj, controllerData, server, headers)

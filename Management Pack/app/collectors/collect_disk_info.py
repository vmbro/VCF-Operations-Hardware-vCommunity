#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import requests
from constants.system_api_constants import SYSTEM_API_KEYS
import aria.ops.adapter_logging as logging

logger = logging.getLogger(__name__)

NULL_STATUS = "null"

def collect_controller_data(host_obj, controllerId, server, USERNAME, PASSWORD):
    # Push Controller info
    URL = f"{server}{controllerId}"
    controller_response = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
    if controller_response.status_code == 200:
        controller_data = controller_response.json()
        description = controller_data.get('Description') or NULL_STATUS
        driveCount = controller_data.get('Drives@odata.count') or NULL_STATUS
        controllerId = controller_data.get('Id') or NULL_STATUS
        enclosureCount = controller_data.get('Enclosures@odata.count') or NULL_STATUS
        health = controller_data['Status']['Health'] or NULL_STATUS
        state = controller_data['Status']['State'] or NULL_STATUS
        #firmwareVersion = controller_data['StorageControllers'][0]['FirmwareVersion'] or NULL_STATUS
        firmwareVersion = (controller_data.get('StorageControllers', [{}])[0].get('FirmwareVersion', NULL_STATUS))
        #manufacturer = controller_data['StorageControllers'][0]['Manufacturer'] or NULL_STATUS
        manufacturer = (controller_data.get('StorageControllers', [{}])[0].get('Manufacturer', NULL_STATUS))
        #model = controller_data['StorageControllers'][0]['Model'] or NULL_STATUS
        model = (controller_data.get('StorageControllers', [{}])[0].get('model', NULL_STATUS))
        #name = controller_data['StorageControllers'][0]['Name'] or NULL_STATUS
        name = (controller_data.get('StorageControllers', [{}])[0].get('name', NULL_STATUS))
        #speedGbps = controller_data['StorageControllers'][0]['SpeedGbps'] or NULL_STATUS
        speedGbps = (controller_data.get('StorageControllers', [{}])[0].get('speedGbps', NULL_STATUS))

        host_obj.with_property(f"Hardware|Controller|{controllerId}|ID", controllerId)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Description", description)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Drive Count", driveCount)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Enclosure Count", enclosureCount)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Health", health)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|State", state)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Firmware Version", firmwareVersion)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Manufacturer", manufacturer)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Model", model)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Name", name)
        host_obj.with_property(f"Hardware|Controller|{controllerId}|Speed Gbps", speedGbps)

        # Push Physical Disk info
        drives = controller_data.get("Drives", [])
        for drive in drives:
            driveObjId = drive["@odata.id"]
            URL = f"{server}{driveObjId}"
            driveResponse = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)
            if driveResponse.status_code == 200:
                driveData = driveResponse.json()
                driveId = driveData.get('Id') or NULL_STATUS
                blockSizeBytes = driveData.get('BlockSizeBytes') or NULL_STATUS
                capableSpeedGbs = driveData.get('CapableSpeedGbs') or NULL_STATUS
                capacityBytes = f"{driveData.get('CapacityBytes') / 1024**3:.2f} GB" or NULL_STATUS
                description = driveData.get('Description') or NULL_STATUS
                encryptionAbility = driveData.get('EncryptionAbility') or NULL_STATUS
                encryptionStatus = driveData.get('EncryptionStatus') or NULL_STATUS
                failurePredicted = driveData.get('FailurePredicted') or NULL_STATUS
                hotspareType = driveData.get('HotspareType') or NULL_STATUS
                manufacturer = driveData.get('Manufacturer') or NULL_STATUS
                mediaType = driveData.get('MediaType') or NULL_STATUS
                model = driveData.get('Model') or NULL_STATUS
                name = driveData.get('Name') or NULL_STATUS
                negotiatedSpeedGbs = driveData.get('NegotiatedSpeedGbs') or NULL_STATUS
                partNumber = driveData.get('PartNumber') or NULL_STATUS
                predictedMediaLifeLeftPercent = driveData.get('PredictedMediaLifeLeftPercent') or NULL_STATUS
                protocol = driveData.get('Protocol') or NULL_STATUS
                revision = driveData.get('Revision') or NULL_STATUS
                rotationSpeedRPM = driveData.get('RotationSpeedRPM') or NULL_STATUS
                serialNumber = driveData.get('SerialNumber') or NULL_STATUS
                health = driveData['Status']['Health'] or NULL_STATUS
                state = driveData['Status']['State'] or NULL_STATUS
                writeCacheEnabled = driveData.get('WriteCacheEnabled') or NULL_STATUS

                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Name", name)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Id", driveId)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Block Size Bytes", blockSizeBytes)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Capable Speed Gbs", capableSpeedGbs)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Capacity Bytes", capacityBytes)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Description", description)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Encryption Ability", encryptionAbility)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Encryption Status", encryptionStatus)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Failure Predicted", failurePredicted)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Hotspare Type", hotspareType)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Manufacturer", manufacturer)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Media Type", mediaType)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Model", model)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Negotiated Speed Gbs", negotiatedSpeedGbs)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Part Number", partNumber)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Predicted Media Life Left Percent", predictedMediaLifeLeftPercent)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Protocol", protocol)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Revision", revision)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Rotation Speed RPM", rotationSpeedRPM)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Serial Number", serialNumber)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Health", health)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|State", state)
                host_obj.with_property(f"Hardware|Controller|{controllerId}|{name}|Write Cache Enabled", writeCacheEnabled)
            else:
                logger.error(f"Can not found the Physical Disk Endpoint: {driveId}")
    else:
        logger.error(f"Can not collect the storage controller details: {controllerId}")
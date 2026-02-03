#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import requests
import aria.ops.adapter_logging as logging
from aria.ops.event import Criticality
from collectors.collect_redfish_info import collect_redfish_data
from collectors.collect_system_api_info import collect_system_api_data
from collectors.collect_events import collect_event_data
from collectors.collect_os_info import collect_os_data
from collectors.collect_fan_info import collect_fan_data
from collectors.collect_firmware_info import collect_firmware_inventory_data
from collectors.collect_warranty_info import collect_warranty_data
from collectors.collect_disk_info import collect_controller_data
from collectors.collect_network_info import collect_network_data
from collectors.collect_memory_info import collect_memory_data
from collectors.collect_power_info import collect_power_data
from helpers.check_server_prefix import check_server
from helpers.create_redfish_session import create_redfish_session
from concurrent.futures import ThreadPoolExecutor, as_completed
from constants.main import DELL_EMC_SERVER_PREFIX

logger = logging.getLogger("collect_main_data")

REDFISH_WORKERS = 10
REQUEST_TIMEOUT = 15

def fetch_url(session, url):
    return session.get(url, verify=False, timeout=REQUEST_TIMEOUT)


def collect_main_data(physicalServer, username, password, physicalServer_obj, physicalServerConfigFile_obj, delliDracLogMode, dellWarrantyFeature, dellTechDirectURL, dellWarrantyToken=None):
    server = check_server(physicalServer)

    systemsData, redfishData, operatingSystemData, networkData, powerData = None, None, None, None, None
    events = None
    warranty_result = None

    session = requests.Session()
    try:
        token, session_uri = create_redfish_session(server, username, password, physicalServerConfigFile_obj)
        headers = {"X-Auth-Token": token}
        session.headers.update(headers)
    except Exception as e:
        session.close()
        return

    with ThreadPoolExecutor(max_workers=REDFISH_WORKERS) as inner_executor:
        all_futures = {}
        all_futures['systems'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Systems/System.Embedded.1")
        all_futures['redfish'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/")
        all_futures['os'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Managers/System.Embedded.1/Attributes?$select=ServerOS.*")
        all_futures['network'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Managers/iDRAC.Embedded.1/Attributes?$select=CurrentIPv4.*")
        all_futures['fan'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Chassis/System.Embedded.1/ThermalSubsystem/Fans")
        all_futures['firmware'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/UpdateService/FirmwareInventory")
        all_futures['storage'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Systems/System.Embedded.1/Storage")
        all_futures['power_supply'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Chassis/System.Embedded.1/Power")
        all_futures['memory'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Systems/System.Embedded.1/Memory")
        if delliDracLogMode != "Disabled":
            if delliDracLogMode == "Fault List":
                all_futures['events'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/FaultList/Entries")
                logger.info(f"iDRAC Log Mode: Fault List selected for {server}")
            elif delliDracLogMode == "SEL Logs":
                all_futures['events'] = inner_executor.submit(fetch_url, session, f"{server}/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel/Entries")
                logger.info(f"iDRAC Log Mode: SEL Logs selected for {server}")
        else:
            logger.info(f"iDRAC Log Mode is Disabled for {server}, skipping event collection.")

        
        if dellWarrantyFeature == "Enable":
            #client_id = dellClientId
            #client_secret = dellClientSecret
            #url_warranty = dellTechDirectURL
            #dellWarrantyToken = get_dell_warranty_token(dellClientId, dellClientSecret)
            all_futures['warranty'] = inner_executor.submit(
                collect_warranty_data, 
                physicalServer_obj, server, username, password, dellWarrantyToken, dellTechDirectURL
            )
        
        fan_futures, firmware_futures, controller_futures, memory_futures = [], [], [], []
        
        for key, future in all_futures.items():
            try:
                if key == 'warranty':
                    warranty_result = future.result()
                    continue
                
                response = future.result()
                if response.ok:
                    data = response.json()
                    
                    if key == 'systems':
                        systemsData = data
                    elif key == 'redfish':
                        redfishData = data
                    elif key == 'os':
                        operatingSystemData = data
                    elif key == 'network':
                        networkData = data
                    elif key == 'power_supply':
                        powerData = data
                    elif key == 'events':
                        events = data
                    elif key == 'memory': 
                        memoryData = data
                        for dimmMember in memoryData.get("Members", []):
                            dimmPath = dimmMember.get("@odata.id")
                            if dimmPath:
                                url = f"{server}{dimmPath}" 
                                memory_futures.append(inner_executor.submit(fetch_url, session, url))
                                
                    
                    elif key == 'fan':
                        for fanMember in data.get("Members", []):
                            fanPath = fanMember.get("@odata.id")
                            if fanPath:
                                url = f"{server}{fanPath}"
                                fan_futures.append(inner_executor.submit(fetch_url, session, url))
                                
                                
                    elif key == 'firmware':
                        for firmwareMember in data.get("Members", []):
                            firmwarePath = firmwareMember.get("@odata.id")
                            if firmwarePath and firmwarePath.startswith("/redfish/v1/UpdateService/FirmwareInventory/Installed-"):
                                url = f"{server}{firmwarePath}"
                                firmware_futures.append(inner_executor.submit(fetch_url, session, url))
                                
                                
                    elif key == 'storage':
                        controllers = data.get("Members", [])
                        for controller in controllers:
                            controllerId = controller.get("@odata.id")
                            if controllerId:
                                url = f"{server}{controllerId}"
                                controller_futures.append(inner_executor.submit(fetch_url, session, url))                 
            except Exception as exc:
                logger.error(f"Error fetching base API data for {physicalServer} ({key}): {exc}")

        for future in as_completed(fan_futures):
            try:
                response = future.result()
                if response.ok:
                    collect_fan_data(physicalServer_obj, response.json())
            except Exception as exc:
                message = f"{DELL_EMC_SERVER_PREFIX}Error processing Fan data for {physicalServer}: {exc}"
                logger.error(message)
                physicalServerConfigFile_obj.with_event(message = message, criticality=Criticality.CRITICAL)

        for future in as_completed(firmware_futures):
            try:
                response = future.result()
                if response.ok:
                    collect_firmware_inventory_data(physicalServer_obj, response.json())
            except Exception as exc:
                message = f"{DELL_EMC_SERVER_PREFIX}Error processing Firmware data for {physicalServer}: {exc}"
                logger.error(message)
                physicalServerConfigFile_obj.with_event(message = message, criticality=Criticality.CRITICAL)

        for future in as_completed(controller_futures):
            try:
                response = future.result()
                if response.ok:
                    controllerData = response.json()
                    if controllerData.get("Drives"):
                        collect_controller_data(physicalServer_obj, controllerData, server, headers)
            except Exception as exc:
                message = f"{DELL_EMC_SERVER_PREFIX}Error processing Storage Controller data for {physicalServer}: {exc}"
                logger.error(message)
                physicalServerConfigFile_obj.with_event(message = message, criticality=Criticality.CRITICAL)

        for future in as_completed(memory_futures):
            try:
                response = future.result()
                if response.ok:
                    dimmData = response.json()
                    collect_memory_data(physicalServer_obj, dimmData) 
            except Exception as exc:
                message = f"{DELL_EMC_SERVER_PREFIX}Error processing Memory data for {physicalServer}: {exc}"
                logger.error(message)
                physicalServerConfigFile_obj.with_event(message = message, criticality=Criticality.WARNING)
    
    try:
        session.delete(f"{server}{session_uri}", verify=False) 
        session.close() 
    except Exception as e:
        logger.error(f"Error closing Redfish session for {physicalServer}: {e}")

    # Send collected data to VCF Operations
    try:
        collect_system_api_data(physicalServer_obj, systemsData)
        collect_redfish_data(physicalServer_obj, redfishData)
        collect_os_data(physicalServer_obj, operatingSystemData)
        collect_network_data(physicalServer_obj, networkData)
        collect_power_data(physicalServer_obj, powerData)
        if events and "Members" in events:
            for event in events["Members"]:
                if event["Message"] != "Log cleared.":
                    collect_event_data(physicalServer_obj, event)
    except Exception as e:
        message = f"{DELL_EMC_SERVER_PREFIX}Something went wrong during data collection for {physicalServer}: {e}"
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Full Traceback: {error_details}")
        logger.debug(message)
        physicalServerConfigFile_obj.with_event(message = message, criticality=Criticality.WARNING)
#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven
import requests
import time
from datetime import datetime, timezone
import aria.ops.adapter_logging as logging
from aria.ops.event import Criticality
from constants.main import DELL_EMC_SERVER_PREFIX

logger = logging.getLogger("collect_warranty_info")

#Get Service Tag from iDRAC Redfish ---
def get_service_tag(SERVER, USERNAME, PASSWORD):
    url = f"{SERVER}/redfish/v1"
    r = requests.get(url, auth=(USERNAME, PASSWORD), verify=False)
    r.raise_for_status()
    data = r.json()
    serviceTag = data["Oem"]["Dell"]["ServiceTag"]
    if serviceTag:
        logger.info(f"Service Tag has been found for {SERVER}: {serviceTag}")
    else:
        logger.warning(f"Service Tag could not be found for {SERVER}")
    return serviceTag


# Get Dell TechDirect API Token ---
#def get_dell_token(client_id, client_secret):
#    url = "https://api.dell.com/auth/oauth/v2/token"
#    payload = {
#        "grant_type": "client_credentials",
#        "client_id": client_id,
#        "client_secret": client_secret
#    }
#    headers = {"Content-Type": "application/x-www-form-urlencoded"}
#    r = requests.post(url, data=payload, headers=headers)
#    r.raise_for_status()
#    logger.info("Dell TechDirect API token has been retrieved.")
#    return r.json()["access_token"]

# Query Dell TechDirect API ---

def get_warranty_info(access_token, service_tag, url, host_obj):
    if not service_tag:
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    params = {"servicetags": service_tag}

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 429:
                wait_time = (attempt + 1) * 10
                logger.warning(f"Rate Limit hit (429) Service Tag: {service_tag} - Attempt {attempt+1}/{max_retries}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            data = response.json()
            if not data or "entitlements" not in data[0]:
                logger.warning("Cannot find entitlement information from Dell TechDirect API. Skipping warranty info collection.")
                return None

            entitlements = data[0]["entitlements"]
            if not entitlements:
                logger.warning("Entitlement list is empty from Dell TechDirect API. Skipping warranty info collection.")
                return None

            startDate = entitlements[-1].get("startDate")
            endDate = entitlements[-1].get("endDate")
            entitlementType = entitlements[-1].get("entitlementType")
            serviceLevelCode = entitlements[-1].get("serviceLevelCode")
            #serviceLevelDescription = entitlements[-1].get("serviceLevelDescription")
            serviceLevelGroup = entitlements[-1].get("serviceLevelGroup")
            shipDate = data[0]["shipDate"]
            numberOfDaysLeft = datetime.fromisoformat(endDate)
            now = datetime.now(timezone.utc)
            numberOfDaysLeft = (numberOfDaysLeft - now).days
            if numberOfDaysLeft <= 0:
                host_obj.with_metric("Summary|Warranty|Days Left", 0)
            else:
                host_obj.with_metric("Summary|Warranty|Days Left", numberOfDaysLeft)
            host_obj.with_property("Summary|Warranty|Start Date", startDate)
            host_obj.with_property("Summary|Warranty|End Date", endDate)
            host_obj.with_property("Summary|Warranty|Ship Date", shipDate)
            host_obj.with_property("Summary|Warranty|Entitlement Type ", entitlementType)
            host_obj.with_property("Summary|Warranty|Service Level|Code", serviceLevelCode)
            #host_obj.with_property("Summary|Warranty|Service Level|Description", serviceLevelDescription)
            host_obj.with_property("Summary|Warranty|Service Level|Group", serviceLevelGroup)
            logger.info(f"Warranty informations have been pushed from Dell TechDirect API for Service Tag: {service_tag}")
            
            return True  # Successful execution, exit the function
        
        except Exception as e:
            logger.warning(f"Error getting warranty information from Dell TechDirect API. URL: {url} error: {e}")

def collect_warranty_data(host_obj, SERVER, USERNAME, PASSWORD, dellWarrantyToken, url):
    serviceTag = get_service_tag(SERVER, USERNAME, PASSWORD)
    if serviceTag:
        get_warranty_info(dellWarrantyToken, serviceTag, url, host_obj)
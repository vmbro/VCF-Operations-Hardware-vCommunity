#  Copyright 2026 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import requests
import aria.ops.adapter_logging as logging

logger = logging.getLogger("get_dell_warranty_token")

def get_dell_warranty_token(client_id, client_secret):
    url = "https://api.dell.com/auth/oauth/v2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, data=payload, headers=headers)
    r.raise_for_status()
    logger.info("Dell TechDirect API token has been retrieved.")
    return r.json()["access_token"]
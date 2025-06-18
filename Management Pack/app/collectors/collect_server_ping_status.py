#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import time
from ping3 import ping
import aria.ops.adapter_logging as logging

logger = logging.getLogger(__name__)


def pingIP(ip_address):
    try:
        for attempt in range(3):
            logger.info(f"Attempt {attempt + 1} to ping {ip_address}...")
            results = []

            for _ in range(4):
                delay = ping(ip_address, timeout=4, unit='ms')
                if delay is not None and delay is not False:
                    results.append(delay)

            if results:
                min_time = min(results)
                max_time = max(results)
                avg_time = sum(results) / len(results)
                stddev_time = (sum((x - avg_time) ** 2 for x in results) / len(results)) ** 0.5
                packet_loss = int(((4 - len(results)) / 4) * 100)
                pingStatus = 1

                metrics = {
                    "packet_loss": packet_loss,
                    "min_time": round(min_time, 3),
                    "avg_time": round(avg_time, 3),
                    "max_time": round(max_time, 3),
                    "stddev_time": round(stddev_time, 3),
                    "pingStatus": pingStatus
                }
                return metrics
            else:
                pingStatus = 0

            if attempt < 3:
                time.sleep(10)
        pingStatus = 0
        logger.info("All attempts to ping failed.")
        return pingStatus
    except OSError:
        pingStatus = 0
        return pingStatus
    except:
        logger.debug("A general error occurred. Check your IP list configuration.")


def collect_ping_data(host_obj):
    host_objJSON = host_obj.get_json()
    keys = host_objJSON['key']
    hostName = keys['name']

    getPingResult = pingIP(hostName)
    if getPingResult != None and getPingResult != 0:
        packet_loss = getPingResult["packet_loss"]
        min_time = getPingResult["min_time"]
        avg_time = getPingResult["avg_time"]
        max_time = getPingResult["max_time"]
        stddev_time = getPingResult["stddev_time"]
        pingStatus = getPingResult["pingStatus"]

        # Add metrics to host object
        host_obj.with_metric("Availability|Ping|PacketLoss (%)", packet_loss)
        host_obj.with_metric("Availability|Ping|Min (ms)", min_time)
        host_obj.with_metric("Availability|Ping|Avg (ms)", avg_time)
        host_obj.with_metric("Availability|Ping|Max (ms)", max_time)
        host_obj.with_metric("Availability|Ping|Stddev (ms)", stddev_time)
        host_obj.with_metric("Availability|Ping|Status", pingStatus)
    else:
        host_obj.with_metric("Availability|Ping|Status", 0)
#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import time
from ping3 import ping
import aria.ops.adapter_logging as logging

logger = logging.getLogger(__name__)

def pingIP(ip_address):
    ping_metrics = {
        "packet_loss": 100,
        "min_time": 0.0,
        "avg_time": 0.0,
        "max_time": 0.0,
        "stddev_time": 0.0,
        "pingStatus": 0
    }

    maxAttempts = 3
    packetCount = 4
    timeoutDuration = 2
    sleepBetweenAttempts = 2

    try:
        for attempt in range(maxAttempts):
            logger.info(f"Attempt {attempt + 1} for {ip_address}...")
            results = []

            for _ in range(packetCount):
                delay = ping(ip_address, timeout=timeoutDuration, unit='ms')
                if delay is not None and delay is not False:
                    results.append(delay)

            if results:
                avg_time = sum(results) / len(results)
                ping_metrics.update({
                    "packet_loss": round(((packetCount - len(results)) / packetCount) * 100, 2),
                    "min_time": round(min(results), 3),
                    "avg_time": round(avg_time, 3),
                    "max_time": round(max(results), 3),
                    "stddev_time": round((sum((x - avg_time) ** 2 for x in results) / len(results)) ** 0.5, 3),
                    "pingStatus": 1
                })
                logger.info(f"Ping successful for {ip_address} on attempt {attempt + 1}")
                return ping_metrics
            
            if attempt < maxAttempts - 1:
                logger.info(f"Attempt {attempt + 1} failed for {ip_address}, sleeping {sleepBetweenAttempts}s...")
                time.sleep(sleepBetweenAttempts)
        
        logger.warning(f"All {maxAttempts} attempts failed for {ip_address}.")
        return ping_metrics

    except Exception as e:
        logger.error(f"General error pinging {ip_address}: {str(e)}")
        return ping_metrics

def collect_ping_data(physicalServer_obj, physicalServer):
    result = pingIP(physicalServer)
    packetLoss = result["packet_loss"]
    minTime = result["min_time"]
    avgTime = result["avg_time"]
    maxTime = result["max_time"]
    stddevTime = result["stddev_time"]
    pingStatus = result["pingStatus"]

    physicalServer_obj.with_metric("Availability|Ping|Status", pingStatus)
    physicalServer_obj.with_metric("Availability|Ping|PacketLoss", packetLoss)
    physicalServer_obj.with_metric("Availability|Ping|Min", minTime)
    physicalServer_obj.with_metric("Availability|Ping|Avg", avgTime)
    physicalServer_obj.with_metric("Availability|Ping|Max", maxTime)
    physicalServer_obj.with_metric("Availability|Ping|Stddev", stddevTime)
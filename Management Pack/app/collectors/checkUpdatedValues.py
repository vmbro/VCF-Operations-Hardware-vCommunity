#  Copyright 2025 Hardware vCommunity MP
#  Author: Onur Yuzseven onur.yuzseven@broadcom.com

import logging

NULL_STATUS = "null"
logger = logging.getLogger(__name__)


def checkLastValue(objectName, keyName, currentValue, valueType):
      if valueType == "property":
            lastValue = objectName.get_last_property_value(keyName)
            if lastValue != currentValue:
                  logger.info(f"Property value changed for {keyName}: from '{lastValue}' to '{currentValue}'")
                  return True
            else:
                  logger.info(f"No change in property value for {keyName}: from '{lastValue}' remains as '{currentValue}'")
                  return False
      else:
            logger.info("ValueType is not property!")
#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven
#import json
import logging
from constants.main import ADAPTER_KIND
from constants.main import ORGANIZATION
from constants.main import ORGANIZATION_IDENTIFIER
from constants.main import PHYSICAL_DATACENTER
from constants.main import PHYSICAL_DATACENTER_IDENTIFIER
from constants.main import PHYSICAL_SERVER
from constants.main import PHYSICAL_SERVER_IDENTIFIER
from aria.ops.object import Identifier
from aria.ops.object import Object
from aria.ops.object import Key
from helpers.create_object_key import create_object_key
from helpers.create_object import create_object

logger = logging.getLogger(__name__)


def check_object_status(adapter_instance, objectType, objectName, objectIdentifierName, objectIdentifierValue, result):
    with adapter_instance.suite_api_client as suite_api:
        resources = suite_api.query_for_resources(
            query={
                "adapterKind": [ADAPTER_KIND],
                "resourceKind": [objectType],
                "name": [objectName],
            }
        )

    objectList: list[Object] = []
    for obj in resources:
        identifierValue = obj.get_identifier_value(objectIdentifierName)
        #logger.error(f"obj.get_json(): {obj.get_json()}")
        if identifierValue == objectIdentifierValue:
            objectList.append(obj)
            break

    if len(objectList) == 1:
        if objectList:
            obj = objectList[0]
            result.add_object(obj)
        #logger.info(f"{objectIdentifierValue} already exists in {ADAPTER_KIND} adapter.")

        return obj
    
    elif len(objectList) == 0:
        logger.info(f"No {objectType} object type found with {objectIdentifierValue} identifier. New {objectType} object will be created.")
        return "createNewObject"
    else:
        errorMessage = (f"{objectIdentifierValue} identifier might be duplicated. {objectType} must be unique.")
        logger.debug(errorMessage)

        return False
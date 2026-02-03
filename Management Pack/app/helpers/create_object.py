#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import logging
from constants.main import ADAPTER_KIND
from aria.ops.object import Identifier

logger = logging.getLogger(__name__)


def create_object(objectName, objectType, objectIdentifier, objectIdentifierValue, result):
    if isinstance(objectIdentifierValue, list):
        obj = result.object(adapter_kind=ADAPTER_KIND, object_kind=objectType, name=objectName, identifiers=objectIdentifierValue)
        result.add_object(obj)
        logger.info(f"Created new {objectName} {objectType} object in {ADAPTER_KIND} adapter.")

        return obj
    else:
        obj = result.object(adapter_kind=ADAPTER_KIND, object_kind=objectType, name=objectName, identifiers=[Identifier(objectIdentifier, objectIdentifierValue)])
        result.add_object(obj)
        logger.info(f"Created new {objectName} {objectType} object in {ADAPTER_KIND} adapter.")

        return obj


    #obj = result.object(adapter_kind=ADAPTER_KIND, object_kind=objectType, name=objectName, identifiers=[Identifier(objectIdentifier, objectIdentifierValue)])
    #result.add_object(obj)
    #logger.info(f"Created new {objectName} {objectType} object in {ADAPTER_KIND} adapter.")
#
    #return obj
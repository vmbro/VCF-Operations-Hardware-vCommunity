#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import logging
from aria.ops.object import Key
from aria.ops.object import Identifier
from constants.main import ADAPTER_KIND

logger = logging.getLogger(__name__)

def create_object_key(objectKind, name, objectIdentifier, objectIdentifierValue):
    if isinstance(objectIdentifierValue, list):
        objectKey = Key(
            adapter_kind=ADAPTER_KIND,
            object_kind=objectKind,
            name=name,
            identifiers=objectIdentifierValue
        )
        if objectKey:
            logger.info(f"Object key has been generated successfuly for {name}")
            return objectKey
        else:
            logger.info(f"Failed to generate Object key for {name}")
    else:
        objectKey = Key(
            adapter_kind=ADAPTER_KIND,
            object_kind=objectKind,
            name=name,
            identifiers=[ Identifier(objectIdentifier, objectIdentifierValue) ]
        )
        if objectKey:
            logger.info(f"Object key has been generated successfuly for {name}")
            return objectKey
        else:
            logger.info(f"Failed to generate Object key for {name}")






    #objectKey = Key(
    #    adapter_kind=ADAPTER_KIND,
    #    object_kind=objectKind,
    #    name=name,
    #    identifiers=[ Identifier(objectIdentifier, objectIdentifierValue) ]
    #)
    #if objectKey:
    #    logger.info(f"Object key has been generated successfuly for {name}")
    #    return objectKey
    #else:
    #    logger.info(f"Failed to generate Object key for {name}")


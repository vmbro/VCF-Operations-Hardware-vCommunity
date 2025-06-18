#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import sys
from typing import List
import aria.ops.adapter_logging as logging
import requests as requests
from aria.ops.adapter_instance import AdapterInstance
from aria.ops.definition.adapter_definition import AdapterDefinition
from aria.ops.result import CollectResult
from aria.ops.result import EndpointResult
from aria.ops.result import TestResult
from aria.ops.timer import Timer
from constants.main import ADAPTER_KIND
from constants.main import ADAPTER_NAME
from constants.main import USER_CREDENTIAL
from constants.main import PASSWORD_CREDENTIAL
import xml.etree.ElementTree as ET
from collectors.collect_main_info import collect_main_data
from collectors.collect_server_ping_status import collect_ping_data

logger = logging.getLogger(__name__)


def get_adapter_definition() -> AdapterDefinition:
    with Timer(logger, "Get Adapter Definition"):
        definition = AdapterDefinition(ADAPTER_KIND, ADAPTER_NAME)

        definition.define_string_parameter(
            "configFile",
            label="Configuration File Name",
            description="Enter the configuration file name that contains Dell Server FQDN/IP list. Usage: SolutionConfig/config_file_name",
            default="SolutionConfig/your_configuration_file_name",
            required=True,
        )

        definition.define_string_parameter(
            "datacenter",
            label="Datacenter",
            description="Enter the datacenter name to group Dell servers.",
            default="Istanbul",
            required=True,
        )

        definition.define_int_parameter(
            "container_memory_limit",
            label="Adapter Memory Limit (MB)",
            description="Sets the maximum amount of memory VMware Aria Operations can "
            "allocate to the container running this adapter instance.",
            required=True,
            advanced=True,
            default=1024,
        )

        credential = definition.define_credential_type("Credential", "Credential")
        credential.define_string_parameter(USER_CREDENTIAL, "Username")
        credential.define_password_parameter(PASSWORD_CREDENTIAL, "Password")

        #server = definition.define_object_type("Server", "Server")
        #server.define_string_property("hostname", "Hostname")

        logger.debug(f"Returning adapter definition: {definition.to_json()}")
        return definition



def get_configFile(adapter_instance: AdapterInstance) -> str:
    configFile = adapter_instance.get_identifier_value("configFile")
    return configFile


def get_credential(adapter_instance: AdapterInstance) -> str:
    username = adapter_instance.get_credential_value(USER_CREDENTIAL)
    password = adapter_instance.get_credential_value(PASSWORD_CREDENTIAL)
    return username, password

def get_datacenter(adapter_instance: AdapterInstance) -> str:
    datacenter = adapter_instance.get_identifier_value("datacenter")
    return datacenter

def get_endpointURL(adapter_instance: AdapterInstance) -> str:
    configFile = get_configFile(adapter_instance)
    apiPath = f"api/configurations/files?path={configFile}"
    with adapter_instance.suite_api_client as suite_api:
        getConfigFile = suite_api.get(url = apiPath)

    IP_List = getConfigFile.text
    parsedResponse = ET.fromstring(IP_List)
    ip_addr = parsedResponse.text.strip().split(',')
    hosts = []
    for ip in ip_addr:
        endpoint = ip.strip()
        if not endpoint.startswith("https"):
            endpoint = f"https://{endpoint}"
            hosts.append(endpoint)
    return hosts
    

def test(adapter_instance: AdapterInstance) -> TestResult:
    with Timer(logger, "Test"):
        result = TestResult()
        try:
            #SuiteAPI doesn't work out of Collect() method
            logger.info("SuiteAPI doesn't work out of Collect() method")

        except Exception as e:
            logger.error("Unexpected connection test error")
            logger.exception(e)
            result.with_error("Unexpected connection test error: " + repr(e))
        finally:
            calledByTestFunc = False
            logger.debug(f"Returning test result: {result.get_json()}")
            return result


def collect(adapter_instance: AdapterInstance) -> CollectResult:
    with Timer(logger, "Collection"):
        result = CollectResult()
        try:
            configFile = get_configFile(adapter_instance)
            apiPath = f"api/configurations/files?path={configFile}"
            with adapter_instance.suite_api_client as suite_api:
                getConfigFile = suite_api.get(url = apiPath)
   
            IP_List = getConfigFile.text
            parsedResponse = ET.fromstring(IP_List)
            ip_addr = parsedResponse.text.strip().split(',')
            hosts = []
            for ip in ip_addr:
                hosts.append(ip.strip())
            username, password = get_credential(adapter_instance)
            datacenter = get_datacenter(adapter_instance)
            datacenter_obj = result.object(ADAPTER_KIND, "Datacenter", datacenter)
            for host in hosts:
                host_obj = result.object(ADAPTER_KIND, "Host", host)
                datacenter_obj.add_child(host_obj)
                collect_main_data(host, username, password, host_obj, datacenter)
                collect_ping_data(host_obj)

        except Exception as e:
            logger.error("Unexpected collection error")
            logger.exception(e)
            result.with_error("Unexpected collection error: " + repr(e))
        finally:
            logger.debug(f"Returning collection result {result.get_json()}")
            return result


def get_endpoints(adapter_instance: AdapterInstance) -> EndpointResult:
    with Timer(logger, "Get Endpoints"):
        result = EndpointResult()
        endpointURLs = get_endpointURL(adapter_instance)
        for endpointURL in endpointURLs:
            result.with_endpoint(endpointURL)
        logger.debug(f"Returning endpoints: {result.get_json()}")
        return result


def main(argv: List[str]) -> None:
    logging.setup_logging("adapter.log")
    logging.rotate()
    logger.info(f"Running adapter code with arguments: {argv}")
    if len(argv) != 3:
        logger.error("Arguments must be <method> <inputfile> <ouputfile>")
        exit(1)

    method = argv[0]
    try:
        if method == "test":
            test(AdapterInstance.from_input()).send_results()
        elif method == "endpoint_urls":
            get_endpoints(AdapterInstance.from_input()).send_results()
        elif method == "collect":
            collect(AdapterInstance.from_input()).send_results()
        elif method == "adapter_definition":
            result = get_adapter_definition()
            if type(result) is AdapterDefinition:
                result.send_results()
            else:
                logger.info(
                    "get_adapter_definition method did not return an AdapterDefinition"
                )
                exit(1)
        else:
            logger.error(f"Command {method} not found")
            exit(1)
    finally:
        logger.info(Timer.graph())


if __name__ == "__main__":
    main(sys.argv[1:])
#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import concurrent.futures
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
from aria.ops.object import Identifier
from aria.ops.event import Criticality
from aria.ops.definition.units import Units
from constants.main import ADAPTER_KIND
from constants.main import ADAPTER_NAME
from constants.main import USER_CREDENTIAL
from constants.main import PASSWORD_CREDENTIAL
from constants.main import CONFIG_FILE
from constants.main import CONFIG_FILE_IDENTIFIER
from constants.main import PHYSICAL_SERVER
from constants.main import PHYSICAL_SERVER_IDENTIFIER
from constants.main import PHYSICAL_SERVER_CONFIG_FILE_PARAMETER
#from constants.main import CONFIG_FILE_PARAMETER
from constants.main import DELL_WARRANTY_CHECKER_PARAMETER
from constants.main import DELL_TECHDIRECT_URL_PARAMETER
from constants.main import DELL_IDRAC_LOG_MODE_PARAMETER
from constants.main import CONTAINER_MEMORY_LIMIT_PARAMETER
from constants.main import DELL_CLIENT_ID_PARAMETER
from constants.main import DELL_CLIENT_SECRET_PARAMETER
from constants.main import MAX_WORKERS_PARAMETER
from constants.main import PING_WORKERS_PARAMETER
from constants.main import ADAPTER_MODE_PARAMETER
import xml.etree.ElementTree as ET
from helpers.object_checker import check_object_status
from collectors.collect_main_info import collect_main_data
from collectors.collect_server_ping_status import collect_ping_data
from helpers.get_dell_warranty_token import get_dell_warranty_token


logger = logging.getLogger(__name__)


def get_adapter_definition() -> AdapterDefinition:
    with Timer(logger, "Get Adapter Definition"):
        definition = AdapterDefinition(ADAPTER_KIND, ADAPTER_NAME)

        definition.define_string_parameter(
            PHYSICAL_SERVER_CONFIG_FILE_PARAMETER,
            label="Physical Server Config File",
            description="Enter the configuration file name that contains physical server FQDN/IP list.",
            required=True,
        )

        #definition.define_string_parameter(
        #    CONFIG_FILE_PARAMETER,
        #    label="Physical Datacenter Name",
        #    description="Enter the datacenter name to group Dell servers.",
        #    required=True,
        #)

        definition.define_enum_parameter(
            DELL_IDRAC_LOG_MODE_PARAMETER,
            values=["Fault List", "SEL Logs", "Disabled"],
            label="Dell iDRAC Log Monitoring",
            description="Choose iDRAC log type to monitor server events.",
            default="Fault List",
            required=False,
            advanced=True,
        )
        
        definition.define_enum_parameter(
            DELL_WARRANTY_CHECKER_PARAMETER,
            values=["Enable", "Disable"],
            label="Dell Warranty Checker",
            description="Enable or Disable Dell Warranty Checker feature. This feature requires Dell TechDirect API credentials.",
            default="Disable",
            required=False,
            advanced=True,
        )

        definition.define_string_parameter(
            DELL_TECHDIRECT_URL_PARAMETER,
            label="Dell TechDirect URL",
            description="Enter your Dell TechDirect URL to query warranty information.",
            default="https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements",
            required=False,
            advanced=True,
        )

        definition.define_int_parameter(
            MAX_WORKERS_PARAMETER,
            label="Maximum worker threads for data collection.",
            description="Sets the maximum amount of threads for data collection from physical servers. Maximum is 500.",
            required=False,
            advanced=True,
            default=200,
        )

        definition.define_int_parameter(
            PING_WORKERS_PARAMETER,
            label="Maximum worker threads for ping requests.",
            description="Sets the maximum amount of threads for ping requests. Maximum is 100.",
            required=False,
            advanced=True,
            default=100,
        )

        definition.define_enum_parameter(
            ADAPTER_MODE_PARAMETER,
            values=["PING Only", "Server Monitoring"],
            label="Adapter Mode",
            description="Select adapter mode: PING Only for ping status, Server Monitoring for full physical server data. Default is Server Monitoring mode.",
            default="Server Monitoring",
            required=False,
            advanced=True,
        )

        definition.define_int_parameter(
            CONTAINER_MEMORY_LIMIT_PARAMETER,
            label="Adapter Memory Limit (MB)",
            description="Sets the maximum amount of memory VMware Aria Operations can "
            "allocate to the container running this adapter instance.",
            required=True,
            advanced=True,
            default=1024,
        )

        ### --- Credential Type Definitions --- ###

        credential = definition.define_credential_type("Credential", "Credential")
        credential.define_string_parameter(USER_CREDENTIAL, "Username")
        credential.define_password_parameter(PASSWORD_CREDENTIAL, "Password")
        credential.define_password_parameter(DELL_CLIENT_ID_PARAMETER, "Dell TechDirect Client ID", required=False)
        credential.define_password_parameter(DELL_CLIENT_SECRET_PARAMETER, "Dell TechDirect Client Secret", required=False)

        ### --- Object Type Definitions --- ###

        # Physical Datacenter Object Types, Groups and Metrics
        physicalServerConfigFile = definition.define_object_type(CONFIG_FILE, "Config File")
        physicalServerConfigFile.define_string_identifier(key=CONFIG_FILE_IDENTIFIER,is_part_of_uniqueness=True)
        
        physicalServerConfigFileSummary = physicalServerConfigFile.define_group("Summary", "Summary")
        physicalServerConfigFileSummary.define_metric("Physical Server Count", "Physical Server Count")

        # Physical Server Object Types, Groups and Metrics
        physicalServer = definition.define_object_type(PHYSICAL_SERVER, "Physical Server")
        physicalServer.define_string_identifier(key=PHYSICAL_SERVER_IDENTIFIER, is_part_of_uniqueness=True)

        physicalServerSummary = physicalServer.define_group("Summary", "Summary")
        physicalServerSummary.define_string_property("Hostname", "Hostname")
        physicalServerSummary.define_string_property("Config File", "Config File")
        #physicalServerSummary.define_string_property("Parent Config File", "Parent Datacenter")
        physicalServerSummary.define_string_property("Part Number", "Part Number")
        physicalServerSummary.define_string_property("Server Serial Number", "Server Serial Number")
        physicalServerSummary.define_string_property("Manufacturer", "Manufacturer")
        physicalServerSummary.define_string_property("Server Model", "Server Model")
        physicalServerSummary.define_string_property("Boot Last State", "Boot Last State")

        # Settings
        physicalServerSettings = physicalServer.define_group("Settings", "Settings")
        physicalServerSettings.define_string_property("Power State", "Power State")
        physicalServerSettings.define_string_property("Location Indicator Active", "LocationIndicatorActive")
        physicalServerSettings.define_string_property("CPU State", "CPU State")
        physicalServerSettings.define_string_property("TPM State", "TPM State")
        physicalServerSettings.define_metric("Console Max Concurrent Sessions", "Console Max Concurrent Sessions", unit=Units.MISC.SESSIONS)
        physicalServerSettings.define_string_property("Console Service Enabled", "Console Service Enabled")

        # Settings | BIOS
        physicalServerSettingsBIOS = physicalServerSettings.define_group("BIOS", "BIOS")
        physicalServerSettingsBIOS.define_string_property("Version", "Version")
        physicalServerSettingsBIOS.define_string_property("Override Enabled", "Override Enabled")
        physicalServerSettingsBIOS.define_string_property("Override Mode", "Override Mode")
        physicalServerSettingsBIOS.define_string_property("Stop Boot On Fault", "Stop Boot On Fault")
        physicalServerSettingsBIOS.define_string_property("Release Date", "Release Date")

        # Security
        physicalServerSecurity = physicalServer.define_group("Security", "Security")

        physicalServerSecurityTPM = physicalServerSecurity.define_group("TPM", "TPM")
        physicalServerSecurityTPM.define_string_property("Release Date", "Release Date")
        physicalServerSecurityTPM.define_string_property("Interface Type", "Interface Typee")
        physicalServerSecurityTPM.define_metric("Module Count", "Module Count")

        physicalServerSummaryRedfish = physicalServerSummary.define_group("Redfish", "Redfish")
        physicalServerSummaryRedfish.define_string_property("ID", "ID")
        physicalServerSummaryRedfish.define_string_property("Manager MAC Address", "Manager MAC Address")
        physicalServerSummaryRedfish.define_string_property("Product", "Product")
        physicalServerSummaryRedfish.define_string_property("Redfish Version", "Redfish Version")


        physicalServerSummaryNetwork = physicalServerSummary.define_group("Network", "Network")
        physicalServerSummaryNetwork.define_string_property("IPv4 Address", "IPv4 Address")
        physicalServerSummaryNetwork.define_string_property("DHCP Enable", "DHCP Enable")
        physicalServerSummaryNetwork.define_string_property("DNS 1", "DNS 1")
        physicalServerSummaryNetwork.define_string_property("DNS 2", "DNS 2")
        physicalServerSummaryNetwork.define_string_property("DNS From DHCP", "DNS From DHCP")
        physicalServerSummaryNetwork.define_string_property("IPv4 Enable", "IPv4 Enable")
        physicalServerSummaryNetwork.define_string_property("Gateway", "Gateway")
        physicalServerSummaryNetwork.define_string_property("Netmask", "Netmask")


        physicalServerSummaryOperatingSystem = physicalServerSummary.define_group("Operating System", "Operating System")
        physicalServerSummaryOperatingSystem.define_string_property("Name", "Name")
        physicalServerSummaryOperatingSystem.define_string_property("Version", "Version")
        physicalServerSummaryOperatingSystem.define_metric("Powered on Time", "Powered On Time", unit=Units.TIME.DAYS)
        #physicalServerSummaryOperatingSystem.define_string_property("Product Key", "Product Key")

        # Physical Server Firmware
        physicalServerFirmware = physicalServer.define_instanced_group("Firmware", "Firmware", instance_required=True)
        physicalServerFirmware.define_string_property("Version", "Version")

        # Physical Server Warranty
        physicalServerSummaryWarranty = physicalServerSummary.define_group("Warranty", "Warranty")
        physicalServerSummaryWarranty.define_metric("Days Left", "Days Left", unit=Units.TIME.DAYS)
        physicalServerSummaryWarranty.define_string_property("Start Date", "Start Date")
        physicalServerSummaryWarranty.define_string_property("End Date", "End Date")
        physicalServerSummaryWarranty.define_string_property("Ship Date", "Ship Date")
        physicalServerSummaryWarranty.define_string_property("Entitlement Type ", "Entitlement Type ")

        # Physical Server Warranty Service Level
        physicalServerSummaryWarrantyServiceLevel = physicalServerSummaryWarranty.define_group("Service Level", "Service Level")
        physicalServerSummaryWarrantyServiceLevel.define_string_property("Code", "Code")
        physicalServerSummaryWarrantyServiceLevel.define_string_property("Description", "Description")
        physicalServerSummaryWarrantyServiceLevel.define_string_property("Group", "Group")

        # Physical Server Hardware Object Types, Groups and Metrics
        physicalServerHardware = physicalServer.define_group("Hardware", "Hardware")

        physicalServerHardwareChassis = physicalServerHardware.define_group("Chassis", "Chassis")
        physicalServerHardwareChassis.define_metric("Power Supply Count", "Power Supply Count")
        physicalServerHardwareChassis.define_metric("PCIe Devices Count", "PCIe Devices Count")
        physicalServerHardwareChassis.define_metric("Populated DIMM Slots", "Populated DIMM Slots")
        physicalServerHardwareChassis.define_metric("Populated PCIe Slots", "Populated PCIe Slots")
        physicalServerHardwareChassis.define_metric("Estimated Exhaust Temperature", "Estimated Exhaust Temperature", unit=Units.TEMPERATURE.C)
        physicalServerHardwareChassis.define_metric("Total System Memory", "Total System Memory", unit=Units.DATA_SIZE.GIBIBYTE)
        physicalServerHardwareChassis.define_string_property("Service Tag", "Service Tag")
        physicalServerHardwareChassis.define_string_property("Managed System Size", "Managed System Size")
        physicalServerHardwareChassis.define_string_property("Express Service Code", "Express Service Code")
        physicalServerHardwareChassis.define_string_property("Is OEM Branded", "Is OEM Branded")
        physicalServerHardwareChassis.define_string_property("Max CPU Sockets", "Max CPU Sockets")
        physicalServerHardwareChassis.define_string_property("Max DIMM Slots", "Max DIMM Slots")
        physicalServerHardwareChassis.define_string_property("Max PCIe Slots", "Max PCIe Slots")
        physicalServerHardwareChassis.define_string_property("Memory Operation Mode", "Memory Operation Mode")
        physicalServerHardwareChassis.define_string_property("System Generation", "System Generation")
        physicalServerHardwareChassis.define_string_property("System Memory Error Methodology", "System Memory Error Methodology")
        physicalServerHardwareChassis.define_string_property("Last System Inventory Time", "Last System Inventory Time")
        physicalServerHardwareChassis.define_string_property("Last Update Time", "Last Update Time")
        physicalServerHardwareChassis.define_string_property("Last Reset Time", "Last Reset Time")
        

        physicalServerHardwareController = physicalServerHardware.define_group("Controller", "Controller")

        physicalServerHardwareControllerPhysicalDisks = physicalServerHardwareController.define_instanced_group("Physical Disks", "Physical Disks", instance_required=True)
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Disk Name", "Disk Name")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Disk Block Size", "Disk Block Size", unit=Units.DATA_SIZE.BYTE)
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Capable Speed", "Capable Speed", unit=Units.DATA_RATE.GIGABIT_PER_SECOND)
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Disk Capacity", "Disk Capacity", unit=Units.DATA_SIZE.BYTE)
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Encryption Status", "Encryption Status")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Hotspare Type", "Hotspare Type")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Manufacturer", "Manufacturer")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Disk Media Type", "Disk Media Type")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Disk Model", "Disk Model")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Negotiated Speed", "Negotiated Speed", unit=Units.DATA_RATE.GIGABIT_PER_SECOND)
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Cryptographic Erase Capable", "Cryptographic Erase Capable")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Drive Form Factor", "Drive Form Factor")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Product ID", "Product ID")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("System Erase Capability", "System Erase Capability")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Part Number", "Part Number")
        physicalServerHardwareControllerPhysicalDisks.define_metric("Predicted Media Life Left Percent", "Predicted Media Life Left Percent", unit=Units.RATIO.PERCENT)
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Protocol", "Protocol")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Revision", "Revision")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Drive Serial Number", "Drive Serial Number")
        physicalServerHardwareControllerPhysicalDisks.define_string_property("Drive Health", "Drive Health")


        physicalServerHardwareControllerVolumes = physicalServerHardwareController.define_instanced_group("Volumes", "Volumes", instance_required=True)
        physicalServerHardwareControllerVolumes.define_string_property("Volume Name", "Volume Name")
        physicalServerHardwareControllerVolumes.define_string_property("Volume Block Size", "Volume Block Size", unit=Units.DATA_SIZE.BYTE)
        physicalServerHardwareControllerVolumes.define_string_property("Volume Capacity", "Volume Capacity", unit=Units.DATA_SIZE.BYTE)
        physicalServerHardwareControllerVolumes.define_string_property("Bus Protocol", "Bus Protocol")
        physicalServerHardwareControllerVolumes.define_string_property("Volume Media Type", "Volume Media Type")
        physicalServerHardwareControllerVolumes.define_metric("Remaining Redundancy", "Remaining Redundancy")
        physicalServerHardwareControllerVolumes.define_string_property("Stripe Size", "Stripe Size")
        physicalServerHardwareControllerVolumes.define_string_property("RAID Type", "RAID Type")
        physicalServerHardwareControllerVolumes.define_string_property("Read Cache Policy", "Read Cache Policy")
        physicalServerHardwareControllerVolumes.define_string_property("Volume Health", "Volume Health")
        physicalServerHardwareControllerVolumes.define_string_property("Volume State", "Volume State")
        physicalServerHardwareControllerVolumes.define_string_property("Volume Type", "Volume Type")


        physicalServerHardwareHealth = physicalServerHardware.define_group("Health", "Health")
        physicalServerHardwareHealth.define_string_property("CPU Health", "CPU Health")
        physicalServerHardwareHealth.define_string_property("Battery", "Battery")
        physicalServerHardwareHealth.define_string_property("Cooling", "Cooling")
        physicalServerHardwareHealth.define_string_property("Power Supply", "Power Supply")
        physicalServerHardwareHealth.define_string_property("SEL", "SEL")
        physicalServerHardwareHealth.define_string_property("Storage", "Storage")
        physicalServerHardwareHealth.define_string_property("System", "System")
        physicalServerHardwareHealth.define_string_property("Temperature", "Temperature")
        physicalServerHardwareHealth.define_string_property("Volt", "Volt")
        physicalServerHardwareHealth.define_string_property("Memory Health", "Memory Health")


        physicalServerHardwareCPU = physicalServerHardware.define_group("CPU", "CPU")
        physicalServerHardwareCPU.define_string_property("CPU Model", "CPU Model")
        physicalServerHardwareCPU.define_string_property("Threading Enabled", "Threading Enabled")
        physicalServerHardwareCPU.define_string_property("CPU Count", "CPU Count")
        physicalServerHardwareCPU.define_string_property("Core Count", "Core Count")
        physicalServerHardwareCPU.define_string_property("Logical Processor Count", "Logical Processor Count")


        physicalServerHardwarePower = physicalServerHardware.define_instanced_group("Power", "Power", instance_required=True)
        physicalServerHardwarePower.define_string_property("PS Health", "PS Health")
        physicalServerHardwarePower.define_string_property("PS State", "PS State")
        physicalServerHardwarePower.define_metric("PS Efficiency Percent", "PS Efficiency Percent", unit=Units.RATIO.PERCENT)
        physicalServerHardwarePower.define_string_property("PS Hot Pluggable", "PS Hot Pluggable")
        physicalServerHardwarePower.define_metric("Power Output Watts", "Power Output Watts", unit=Units.POWER.WATT)
        physicalServerHardwarePower.define_metric("Power Input Watts", "Power Input Watts", unit=Units.POWER.WATT)
        physicalServerHardwarePower.define_metric("Last Power Output Watts", "Last Power Output Watts", unit=Units.POWER.WATT)
        physicalServerHardwarePower.define_metric("Line Input Voltage", "Line Input Voltage", unit=Units.VOLTAGE.VOLTS)
        physicalServerHardwarePower.define_string_property("Line Input Voltage Type", "Line Input Voltage Type")
        physicalServerHardwarePower.define_string_property("PS Manufacturer", "PS Manufacturer")
        physicalServerHardwarePower.define_string_property("PS Model", "PS Model")
        physicalServerHardwarePower.define_string_property("PS Part Number", "PS Part Number")
        physicalServerHardwarePower.define_metric("Power Capacity Watts", "Power Capacity Watts", unit=Units.POWER.WATT)
        physicalServerHardwarePower.define_string_property("Power Supply Type", "Power Supply Type")
        physicalServerHardwarePower.define_string_property("PS Serial Number", "PS Serial Number")
        physicalServerHardwarePower.define_metric("Reading Volts", "Reading Volts", unit=Units.VOLTAGE.VOLTS)
        physicalServerHardwarePower.define_string_property("Voltage Health", "Voltage Health")
        physicalServerHardwarePower.define_string_property("Voltage State", "Voltage State")


        physicalServerHardwarePowerInputRanges = physicalServerHardwarePower.define_group("Input Ranges", "Input Ranges")
        physicalServerHardwarePowerInputRanges.define_string_property("Power Input Type", "Power Input Type")
        physicalServerHardwarePowerInputRanges.define_metric("Maximum Frequency", "Maximum Frequency", unit=Units.FREQUENCY.HERTZ)
        physicalServerHardwarePowerInputRanges.define_metric("Maximum Voltage", "Maximum Voltage", unit=Units.VOLTAGE.VOLTS)
        physicalServerHardwarePowerInputRanges.define_metric("Minimum Frequency", "Minimum Frequency", unit=Units.FREQUENCY.HERTZ)
        physicalServerHardwarePowerInputRanges.define_metric("Minimum Voltage", "Minimum Voltage", unit=Units.VOLTAGE.VOLTS)
        physicalServerHardwarePowerInputRanges.define_metric("Output Wattage", "Output Wattage", unit=Units.POWER.WATT)


        # Physical Server Hardware Memory
        physicalServerHardwareMemory = physicalServerHardware.define_instanced_group("Memory", "Memory", instance_required=True)
        physicalServerHardwareMemory.define_string_property("Base Module Type", "Base Module Type")
        physicalServerHardwareMemory.define_string_property("Memory Capacity", "Memory Capacity", unit=Units.DATA_SIZE.MEBIBYTE)
        physicalServerHardwareMemory.define_string_property("Memory Enabled", "Memory Enabled")
        physicalServerHardwareMemory.define_string_property("Error Correction", "Error Correction")
        physicalServerHardwareMemory.define_string_property("Memory Manufacturer", "Memory Manufacturer")
        physicalServerHardwareMemory.define_string_property("Memory Device Type", "Memory Device Type")
        physicalServerHardwareMemory.define_string_property("Memory Type", "Memory Type")
        physicalServerHardwareMemory.define_string_property("Memory Speed", "Memory Speed", unit=Units.FREQUENCY.MEGAHERTZ)
        physicalServerHardwareMemory.define_string_property("Memory Part Number", "Memory Part Number")
        physicalServerHardwareMemory.define_string_property("Rank Count", "Rank Count")
        physicalServerHardwareMemory.define_string_property("Memory Serial Number", "Memory Serial Number")
        physicalServerHardwareMemory.define_string_property("DIMM Health", "DIMM Health")
        physicalServerHardwareMemory.define_string_property("Memory State", "Memory State")


        # Physical Server Hardware Cooler
        physicalServerHardwareCooler = physicalServerHardware.define_group("Cooler", "Cooler")
        physicalServerHardwareCooler.define_metric("Cooler Count", "Cooler Count")

        physicalServerHardwareCoolerFans = physicalServerHardwareCooler.define_instanced_group("Fans", "Fans", instance_required=True)
        physicalServerHardwareCoolerFans.define_string_property("ID", "ID")
        physicalServerHardwareCoolerFans.define_string_property("Fan Health", "Fan Health")
        physicalServerHardwareCoolerFans.define_string_property("State", "State")
        physicalServerHardwareCoolerFans.define_string_property("Hot Pluggable", "Hot Pluggable")
        physicalServerHardwareCoolerFans.define_metric("Speed", "Speed", unit=Units.ROTATION_RATE.RPM)
        physicalServerHardwareCoolerFans.define_string_property("Service Label", "Service Label")
        physicalServerHardwareCoolerFans.define_string_property("Fan Type", "Fan Type")
        physicalServerHardwareCoolerFans.define_metric("Fan PWM", "Fan PWM")


        # Physical Server Availability
        physicalServerAvailability = physicalServer.define_group("Availability", "Availability")

        physicalServerAvailabilityPing = physicalServerAvailability.define_group("Ping", "Ping")
        physicalServerAvailabilityPing.define_metric("PacketLoss", "PacketLoss", unit=Units.RATIO.PERCENT)
        physicalServerAvailabilityPing.define_metric("Min", "Min", unit=Units.TIME.MILLISECONDS)
        physicalServerAvailabilityPing.define_metric("Avg", "Avg", unit=Units.TIME.MILLISECONDS)
        physicalServerAvailabilityPing.define_metric("Max", "Max", unit=Units.TIME.MILLISECONDS)
        physicalServerAvailabilityPing.define_metric("Stddev", "Stddev", unit=Units.TIME.MILLISECONDS)
        physicalServerAvailabilityPing.define_metric("Status", "Status",is_key_attribute=True , is_kpi=True)

        # ------------------------------------------------------------------------ #

        # --- # TODO: define object types --- # 
        

        logger.debug(f"Returning adapter definition: {definition.to_json()}")
        return definition

def get_credential(adapter_instance: AdapterInstance) -> str:
    username = adapter_instance.get_credential_value(USER_CREDENTIAL)
    password = adapter_instance.get_credential_value(PASSWORD_CREDENTIAL)
    return username, password

#def get_datacenter(adapter_instance: AdapterInstance) -> str:
#    datacenter = adapter_instance.get_identifier_value(CONFIG_FILE_PARAMETER)
#    return datacenter

def get_physical_server_configFile(adapter_instance: AdapterInstance) -> str:
    physical_server_configFile = adapter_instance.get_identifier_value(PHYSICAL_SERVER_CONFIG_FILE_PARAMETER)
    return physical_server_configFile

def get_dell_idrac_log_mode_checker(adapter_instance: AdapterInstance) -> str:
    dell_idrac_log_mode = adapter_instance.get_identifier_value(DELL_IDRAC_LOG_MODE_PARAMETER)
    return dell_idrac_log_mode

def get_dell_warranty_checker(adapter_instance: AdapterInstance) -> str:
    dell_warranty_checker = adapter_instance.get_identifier_value(DELL_WARRANTY_CHECKER_PARAMETER)
    return dell_warranty_checker

def get_dell_client_id(adapter_instance: AdapterInstance) -> str:
    dell_client_id = adapter_instance.get_credential_value(DELL_CLIENT_ID_PARAMETER)
    return dell_client_id

def get_dell_client_secret(adapter_instance: AdapterInstance) -> str:
    dell_client_secret = adapter_instance.get_credential_value(DELL_CLIENT_SECRET_PARAMETER)
    return dell_client_secret

def get_dell_techDirect_URL(adapter_instance: AdapterInstance) -> str:
    dell_techDirect_URL = adapter_instance.get_identifier_value(DELL_TECHDIRECT_URL_PARAMETER)
    return dell_techDirect_URL

def get_max_workers(adapter_instance: AdapterInstance) -> str:
    max_workers = adapter_instance.get_identifier_value(MAX_WORKERS_PARAMETER)
    return max_workers

def get_ping_workers(adapter_instance: AdapterInstance) -> str:
    ping_workers = adapter_instance.get_identifier_value(PING_WORKERS_PARAMETER)
    return ping_workers

def get_adapter_mode(adapter_instance: AdapterInstance) -> str:
    adapter_mode = adapter_instance.get_identifier_value(ADAPTER_MODE_PARAMETER)
    return adapter_mode


def get_config_File_data(adapter_instance: AdapterInstance, configFile) -> str:
    apiPath = f"api/configurations/files?path=SolutionConfig/{configFile}"
    with adapter_instance.suite_api_client as suite_api:
        getConfigFile = suite_api.get(url = apiPath)
    lines = getConfigFile.text
    parsedResponse = ET.fromstring(lines)
    formattedLines = parsedResponse.text.strip().split(',')
    objectList = []
    for line in formattedLines:
        objectList.append(line.strip())
    return objectList


def get_endpointURL(adapter_instance: AdapterInstance) -> str:
    configFile = get_physical_server_configFile(adapter_instance)
    apiPath = f"api/configurations/files?path=SolutionConfig/{configFile}"
    with adapter_instance.suite_api_client as suite_api:
        getConfigFile = suite_api.get(url = apiPath)

    IP_List = getConfigFile.text
    parsedResponse = ET.fromstring(IP_List)
    ip_addr = parsedResponse.text.strip().split(',')
    physicalServers = []
    for ip in ip_addr:
        endpoint = ip.strip()
        if not endpoint.startswith("https"):
            endpoint = f"https://{endpoint}"
            physicalServers.append(endpoint)
    return physicalServers
    

def test(adapter_instance: AdapterInstance) -> TestResult:
    with Timer(logger, "Test"):
        result = TestResult()
        try:
            # TODO: Define an ability to test physical server connections
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
    with Timer(logger, f"{ADAPTER_NAME} Collection"):
        result = CollectResult()
        #result.update_relationships = RelationshipUpdateModes.PER_OBJECT
        try:
            with Timer(logger, "Collecting adapter inputs"):
                username, password = get_credential(adapter_instance)
                #physicalServerConfigFile = get_datacenter(adapter_instance)
                dellClientId = get_dell_client_id(adapter_instance)
                dellClientSecret = get_dell_client_secret(adapter_instance)
                dellTechDirectURL = get_dell_techDirect_URL(adapter_instance)
                dellWarrantyFeature = get_dell_warranty_checker(adapter_instance)
                maxWorkers = get_max_workers(adapter_instance)
                pingWorkers = get_ping_workers(adapter_instance)
                delliDracLogMode = get_dell_idrac_log_mode_checker(adapter_instance)
                physicalServerConfigFile = get_physical_server_configFile(adapter_instance)
                physicalServers = get_config_File_data(adapter_instance, physicalServerConfigFile)
                adapterMode = get_adapter_mode(adapter_instance)


            with Timer(logger, "Processing Physical Server Objects"):
                physicalServerConfigFileIdentifier = ADAPTER_KIND + "-" + physicalServerConfigFile
                physicalServerConfigFileObjectStatus = check_object_status(adapter_instance, CONFIG_FILE, physicalServerConfigFile, CONFIG_FILE_IDENTIFIER, physicalServerConfigFileIdentifier, result)
                if physicalServerConfigFileObjectStatus == "createNewObject":
                    physicalServerConfigFile_obj = result.object(adapter_kind=ADAPTER_KIND, object_kind= CONFIG_FILE, name=physicalServerConfigFile, identifiers=[Identifier(CONFIG_FILE_IDENTIFIER, physicalServerConfigFileIdentifier)])
                    #logger.info(f"Created new {physicalServerConfigFile} physical datacenter object in {ADAPTER_KIND} adapter.")
                else:
                    physicalServerConfigFile_obj = physicalServerConfigFileObjectStatus
                    #logger.info(f"Using existing {physicalServerConfigFile} physical datacenter object in {ADAPTER_KIND} adapter.")
                physicalServerConfigFile = get_physical_server_configFile(adapter_instance)
                physicalServers = get_config_File_data(adapter_instance, physicalServerConfigFile)

                physicalServerConfigFile_obj.with_metric("Summary|Physical Server Count", len(physicalServers))

            with Timer(logger, "Processing Physical Servers"):
                MAX_WORKERS = min(int(maxWorkers or 200), 500)
                PING_WORKERS = min(int(pingWorkers or 100), 100)
                
                server_objects = []
                for physicalServer in physicalServers:
                    physicalServerIdentifier = f"{physicalServerConfigFile}-{physicalServer}"

                    physicalServerObjectStatus = check_object_status(adapter_instance, PHYSICAL_SERVER, physicalServer, PHYSICAL_SERVER_IDENTIFIER, physicalServerIdentifier, result)

                    if physicalServerObjectStatus == "createNewObject":
                        physicalServer_obj = result.object(adapter_kind=ADAPTER_KIND, object_kind=PHYSICAL_SERVER, name=physicalServer, identifiers=[Identifier(PHYSICAL_SERVER_IDENTIFIER, physicalServerIdentifier)])
                    else:
                        physicalServer_obj = physicalServerObjectStatus

                    physicalServerConfigFile_obj.add_child(physicalServer_obj)
                    physicalServer_obj.with_property("Summary|Config File", physicalServerConfigFile)
                    server_objects.append((physicalServer, physicalServer_obj))

                
                if dellWarrantyFeature == "Enable":
                    dellWarrantyToken = get_dell_warranty_token(dellClientId, dellClientSecret)

                # --- PING results ---
                logger.info(f"Starting Ping collection for {len(server_objects)} servers...")
                logger.info(f"Using {PING_WORKERS} max workers for ping data collection.")
                with concurrent.futures.ThreadPoolExecutor(max_workers=PING_WORKERS) as ping_executor:
                    ping_futures = [
                        ping_executor.submit(collect_ping_data, obj, name) 
                        for name, obj in server_objects
                    ]

                    for future in concurrent.futures.as_completed(ping_futures):
                        try:
                            future.result()
                        except Exception as exc:
                            logger.error(f"Ping thread error: {exc}")
                    logger.info(f"Finished ping metric collection.")


                if adapterMode == "PING Only":
                    logger.info("Adapter is running in PING Only mode. Skipping main data collection.")
                else:    
                    # --- Physical Server Results ---
                    logger.info(f"Starting Main Data collection for {len(server_objects)} servers...")
                    logger.info(f"Using {MAX_WORKERS} max workers for main data collection.")
                    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as data_executor:
                        main_futures = [
                            data_executor.submit(
                                collect_main_data, 
                                name, username, password, obj, 
                                physicalServerConfigFile_obj, delliDracLogMode, dellWarrantyFeature,
                                dellTechDirectURL, dellWarrantyToken
                            ) 
                            for name, obj in server_objects
                        ]
    
                        for future in concurrent.futures.as_completed(main_futures):
                            try:
                                future.result()
                            except Exception as exc:
                                logger.error(f"Main data collection thread error: {exc}")
                        logger.info(f"Finished physical server data collection.")

        except ET.ParseError as e:
            message = "Failed to parse XML configuration file. Check your configuration file."
            adapter_instance.with_event(message = message, criticality=Criticality.CRITICAL)
            logger.error(message)
            result.with_error(message + repr(e))
            logger.exception(e)
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
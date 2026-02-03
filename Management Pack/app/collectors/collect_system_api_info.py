#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

import aria.ops.adapter_logging as logging

logger = logging.getLogger("collect_system_api_data")

NULL_STATUS = 0
UNKNOWN = "unknown"

def collect_system_api_data(physicalServer_obj, data):
    
    # Summary
    #hostname = data["HostName"] or NULL_STATUS
    hostname = data.get("HostName") or UNKNOWN
    #partNumber = data["PartNumber"] or NULL_STATUS
    partNumber = data.get("PartNumber") or UNKNOWN
    #serialNumber = data["SerialNumber"] or NULL_STATUS
    serialNumber = data.get("SerialNumber") or UNKNOWN
    #manufacturer = data["Manufacturer"] or NULL_STATUS
    manufacturer = data.get("Manufacturer") or UNKNOWN
    #model = data["Model"] or NULL_STATUS
    model = data.get("Model") or UNKNOWN
    #bootLastState = data["BootProgress"]["LastState"] or NULL_STATUS
    bootLastState = data.get("BootProgress", {}).get("LastState") or UNKNOWN

    # Cooler
    #coolerCount = data["Links"]["CooledBy@odata.count"] or NULL_STATUS
    coolerCount = data.get("Links", {}).get("CooledBy@odata.count") or NULL_STATUS

    # Chassis
    #chassisPowerSupplyCount = data["Links"]["PoweredBy@odata.count"] or NULL_STATUS
    #chassisPCIeDevicesCount = data["PCIeDevices@odata.count"] or NULL_STATUS
    #chasisMemoryTotalInstalled = data["MemorySummary"]["TotalSystemMemoryGiB"] or NULL_STATUS
    #chassisServiceTag = data["Oem"]["Dell"]["DellSystem"]["ChassisServiceTag"] or NULL_STATUS
    #chassisManagedSystemSize = data["Oem"]["Dell"]["DellSystem"]["ManagedSystemSize"] or NULL_STATUS
    #chassisEstimatedExhaustTemperature = data["Oem"]["Dell"]["DellSystem"]["EstimatedExhaustTemperatureCelsius"] or NULL_STATUS
    #chassisExpressServiceCode = data["Oem"]["Dell"]["DellSystem"]["ExpressServiceCode"] or NULL_STATUS
    #chassisIsOEMBranded = data["Oem"]["Dell"]["DellSystem"]["IsOEMBranded"] or NULL_STATUS
    #chassisMaxCPUSockets = data["Oem"]["Dell"]["DellSystem"]["MaxCPUSockets"] or NULL_STATUS
    #chassisMaxDIMMSlots = data["Oem"]["Dell"]["DellSystem"]["MaxDIMMSlots"] or NULL_STATUS
    #chassisMaxPCIeSlots = data["Oem"]["Dell"]["DellSystem"]["MaxPCIeSlots"] or NULL_STATUS
    #chassisMemoryOperationMode = data["Oem"]["Dell"]["DellSystem"]["MemoryOperationMode"] or NULL_STATUS
    #chassisPopulatedDIMMSlots = data["Oem"]["Dell"]["DellSystem"]["PopulatedDIMMSlots"] or NULL_STATUS
    #chassisPopulatedPCIeSlots = data["Oem"]["Dell"]["DellSystem"]["PopulatedPCIeSlots"] or NULL_STATUS
    #chassisSystemGeneration = data["Oem"]["Dell"]["DellSystem"]["SystemGeneration"] or NULL_STATUS
    #chassisSysMemErrorMethodology = data["Oem"]["Dell"]["DellSystem"]["SysMemErrorMethodology"] or NULL_STATUS
    #chassisLastSystemInventoryTime = data["Oem"]["Dell"]["DellSystem"]["LastSystemInventoryTime"] or NULL_STATUS
    #chassisLastUpdateTime = data["Oem"]["Dell"]["DellSystem"]["LastUpdateTime"] or NULL_STATUS
    #chassisLastResetTime = data["LastResetTime"] or NULL_STATUS
    chassisPowerSupplyCount = data.get("Links", {}).get("PoweredBy@odata.count") or NULL_STATUS
    chassisPCIeDevicesCount = data.get("PCIeDevices@odata.count") or NULL_STATUS
    chasisMemoryTotalInstalled = data.get("MemorySummary", {}).get("TotalSystemMemoryGiB") or NULL_STATUS
    chassisServiceTag = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("ChassisServiceTag") or UNKNOWN
    chassisManagedSystemSize = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("ManagedSystemSize") or UNKNOWN
    chassisEstimatedExhaustTemperature = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("EstimatedExhaustTemperatureCelsius") or NULL_STATUS
    chassisExpressServiceCode = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("ExpressServiceCode") or UNKNOWN
    chassisIsOEMBranded = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("IsOEMBranded") or UNKNOWN
    chassisMaxCPUSockets = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("MaxCPUSockets") or UNKNOWN
    chassisMaxDIMMSlots = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("MaxDIMMSlots") or UNKNOWN
    chassisMaxPCIeSlots = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("MaxPCIeSlots") or UNKNOWN
    chassisMemoryOperationMode = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("MemoryOperationMode") or UNKNOWN
    chassisPopulatedDIMMSlots = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("PopulatedDIMMSlots") or NULL_STATUS
    chassisPopulatedPCIeSlots = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("PopulatedPCIeSlots") or NULL_STATUS
    chassisSystemGeneration = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("SystemGeneration") or UNKNOWN
    chassisSysMemErrorMethodology = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("SysMemErrorMethodology") or UNKNOWN
    chassisLastSystemInventoryTime = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("LastSystemInventoryTime") or UNKNOWN
    chassisLastUpdateTime = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("LastUpdateTime") or UNKNOWN
    chassisLastResetTime = data.get("LastResetTime") or UNKNOWN
    
    # Settings
    #powerState = data["PowerState"] or NULL_STATUS
    #locationIndicatorActive = data["LocationIndicatorActive"] or NULL_STATUS
    #cpuState = data["ProcessorSummary"]["Status"]["State"] or NULL_STATUS
    #tpmState = data["TrustedModules"][0]["Status"]["State"] or NULL_STATUS
    #graphicMaxConcurrentSessions = data["GraphicalConsole"]["MaxConcurrentSessions"] or NULL_STATUS
    #graphicServiceEnabled = data["GraphicalConsole"]["ServiceEnabled"] or NULL_STATUS
    powerState = data.get("PowerState") or UNKNOWN
    locationIndicatorActive = data.get("LocationIndicatorActive") or UNKNOWN
    cpuState = data.get("ProcessorSummary", {}).get("Status", {}).get("State") or UNKNOWN
    tpmState = data.get("TrustedModules", [{}])[0].get("Status", {}).get("State") or UNKNOWN
    graphicMaxConcurrentSessions = data.get("GraphicalConsole", {}).get("MaxConcurrentSessions") or NULL_STATUS
    graphicServiceEnabled = data.get("GraphicalConsole", {}).get("ServiceEnabled") or UNKNOWN

    # CPU
    #cpuModel = data["ProcessorSummary"]["Model"] or NULL_STATUS
    #cpuThreadingEnabled = data["ProcessorSummary"]["ThreadingEnabled"] or NULL_STATUS
    #cpuCount = data["ProcessorSummary"]["Count"] or NULL_STATUS
    #cpuCoreCount = data["ProcessorSummary"]["CoreCount"] or NULL_STATUS
    #cpuLogicalProcessorCount = data["ProcessorSummary"]["LogicalProcessorCount"] or NULL_STATUS
    cpuModel = data.get("ProcessorSummary", {}).get("Model") or UNKNOWN
    cpuThreadingEnabled = data.get("ProcessorSummary", {}).get("ThreadingEnabled") or UNKNOWN
    cpuCount = data.get("ProcessorSummary", {}).get("Count") or UNKNOWN
    cpuCoreCount = data.get("ProcessorSummary", {}).get("CoreCount") or UNKNOWN
    cpuLogicalProcessorCount = data.get("ProcessorSummary", {}).get("LogicalProcessorCount") or UNKNOWN

    # Health
    #cpuHealthRollup = data["ProcessorSummary"]["Status"]["HealthRollup"] or NULL_STATUS
    #batteryRollupStatus = data["Oem"]["Dell"]["DellSystem"]["BatteryRollupStatus"] or NULL_STATUS
    #coolingRollupStatus = data["Oem"]["Dell"]["DellSystem"]["CoolingRollupStatus"] or NULL_STATUS
    #chassisPSRollupStatus = data["Oem"]["Dell"]["DellSystem"]["PSRollupStatus"] or NULL_STATUS
    #chassisSELRollupStatus = data["Oem"]["Dell"]["DellSystem"]["SELRollupStatus"] or NULL_STATUS
    #chassisStorageRollupStatus = data["Oem"]["Dell"]["DellSystem"]["StorageRollupStatus"] or NULL_STATUS
    #chassisSystemHealthRollupStatus = data["Oem"]["Dell"]["DellSystem"]["SystemHealthRollupStatus"] or None
    #chassisTempRollupStatus = data["Oem"]["Dell"]["DellSystem"]["TempRollupStatus"] or NULL_STATUS
    #chassisVoltRollupStatus = data["Oem"]["Dell"]["DellSystem"]["VoltRollupStatus"] or NULL_STATUS
    #chassisSysMemPrimaryStatus = data["Oem"]["Dell"]["DellSystem"]["SysMemPrimaryStatus"] or NULL_STATUS
    cpuHealthRollup = data.get("ProcessorSummary", {}).get("Status", {}).get("HealthRollup") or UNKNOWN
    batteryRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("BatteryRollupStatus") or UNKNOWN
    coolingRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("CoolingRollupStatus") or UNKNOWN
    chassisPSRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("PSRollupStatus") or UNKNOWN
    chassisSELRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("SELRollupStatus") or UNKNOWN
    chassisStorageRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("StorageRollupStatus") or UNKNOWN
    chassisSystemHealthRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("SystemHealthRollupStatus") or UNKNOWN
    chassisTempRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("TempRollupStatus") or UNKNOWN
    chassisVoltRollupStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("VoltRollupStatus") or UNKNOWN
    chassisSysMemPrimaryStatus = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("SysMemPrimaryStatus") or UNKNOWN

    # BIOS
    #biosVersion = data["BiosVersion"] or NULL_STATUS
    #biosBootSourceOverrideEnabled = data["Boot"]["BootSourceOverrideEnabled"] or NULL_STATUS
    #biosBootSourceOverrideMode = data["Boot"]["BootSourceOverrideMode"] or NULL_STATUS
    #biosStopBootOnFault = data["Boot"]["StopBootOnFault"] or NULL_STATUS
    #biosBIOSReleaseDate = data["Oem"]["Dell"]["DellSystem"]["BIOSReleaseDate"] or NULL_STATUS
    biosVersion = data.get("BiosVersion") or UNKNOWN
    biosBootSourceOverrideEnabled = data.get("Boot", {}).get("BootSourceOverrideEnabled") or UNKNOWN
    biosBootSourceOverrideMode = data.get("Boot", {}).get("BootSourceOverrideMode") or UNKNOWN
    biosStopBootOnFault = data.get("Boot", {}).get("StopBootOnFault") or UNKNOWN
    biosBIOSReleaseDate = data.get("Oem", {}).get("Dell", {}).get("DellSystem", {}).get("BIOSReleaseDate") or UNKNOWN

    # TPM
    #tpmFirmwareVersion = data["TrustedModules"][0]["FirmwareVersion"] or NULL_STATUS
    #tpmInterfaceType = data["TrustedModules"][0]["InterfaceType"] or NULL_STATUS
    #tpmModuleCount = data["TrustedModules@odata.count"] or NULL_STATUS
    tpmFirmwareVersion = data.get("TrustedModules", [{}])[0].get("FirmwareVersion") or UNKNOWN
    tpmInterfaceType = data.get("TrustedModules", [{}])[0].get("InterfaceType") or UNKNOWN
    tpmModuleCount = data.get("TrustedModules@odata.count") or NULL_STATUS

    # Summary
    physicalServer_obj.with_property("Summary|Hostname", hostname)
    physicalServer_obj.with_property("Summary|Part Number", partNumber)
    physicalServer_obj.with_property("Summary|Server Serial Number", serialNumber)
    physicalServer_obj.with_property("Summary|Manufacturer", manufacturer)
    physicalServer_obj.with_property("Summary|Server Model", model)
    physicalServer_obj.with_property("Summary|Boot Last State", bootLastState)

    # Cooler
    physicalServer_obj.with_metric("Hardware|Cooler|Cooler Count", coolerCount)

    # Chassis
    physicalServer_obj.with_metric("Hardware|Chassis|Power Supply Count", chassisPowerSupplyCount)
    physicalServer_obj.with_metric("Hardware|Chassis|PCIe Devices Count", chassisPCIeDevicesCount)
    physicalServer_obj.with_metric("Hardware|Chassis|Total System Memory", chasisMemoryTotalInstalled)
    physicalServer_obj.with_property("Hardware|Chassis|Service Tag", chassisServiceTag)
    physicalServer_obj.with_property("Hardware|Chassis|Managed System Size", chassisManagedSystemSize)
    physicalServer_obj.with_metric("Hardware|Chassis|Estimated Exhaust Temperature", chassisEstimatedExhaustTemperature)
    physicalServer_obj.with_property("Hardware|Chassis|Express Service Code", chassisExpressServiceCode)
    physicalServer_obj.with_property("Hardware|Chassis|Is OEM Branded", chassisIsOEMBranded)
    physicalServer_obj.with_property("Hardware|Chassis|Max CPU Sockets", chassisMaxCPUSockets)
    physicalServer_obj.with_property("Hardware|Chassis|Max DIMM Slots", chassisMaxDIMMSlots)
    physicalServer_obj.with_property("Hardware|Chassis|Max PCIe Slots", chassisMaxPCIeSlots)
    physicalServer_obj.with_property("Hardware|Chassis|Memory Operation Mode", chassisMemoryOperationMode)
    physicalServer_obj.with_metric("Hardware|Chassis|Populated DIMM Slots", chassisPopulatedDIMMSlots)
    physicalServer_obj.with_metric("Hardware|Chassis|Populated PCIe Slots", chassisPopulatedPCIeSlots)
    physicalServer_obj.with_property("Hardware|Chassis|System Generation", chassisSystemGeneration)
    physicalServer_obj.with_property("Hardware|Chassis|System Memory Error Methodology", chassisSysMemErrorMethodology)
    physicalServer_obj.with_property("Hardware|Chassis|Last System Inventory Time", chassisLastSystemInventoryTime)
    physicalServer_obj.with_property("Hardware|Chassis|Last Update Time", chassisLastUpdateTime)
    physicalServer_obj.with_property("Hardware|Chassis|Last Reset Time", chassisLastResetTime)

    # Settings
    physicalServer_obj.with_property("Settings|Power State", powerState)
    physicalServer_obj.with_property("Settings|Location Indicator Active", locationIndicatorActive)
    physicalServer_obj.with_property("Settings|CPU State", cpuState)
    physicalServer_obj.with_property("Settings|TPM State", tpmState)
    physicalServer_obj.with_metric("Settings|Console Max Concurrent Sessions", graphicMaxConcurrentSessions)
    physicalServer_obj.with_property("Settings|Console Service Enabled", graphicServiceEnabled)

    # CPU
    physicalServer_obj.with_property("Hardware|CPU|CPU Model", cpuModel)
    physicalServer_obj.with_property("Hardware|CPU|Threading Enabled", cpuThreadingEnabled)
    physicalServer_obj.with_property("Hardware|CPU|CPU Count", cpuCount)
    physicalServer_obj.with_property("Hardware|CPU|Core Count", cpuCoreCount)
    physicalServer_obj.with_property("Hardware|CPU|Logical Processor Count", cpuLogicalProcessorCount)

    # Health
    physicalServer_obj.with_property("Hardware|Health|CPU Health", cpuHealthRollup)
    physicalServer_obj.with_property("Hardware|Health|Battery", batteryRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|Cooling", coolingRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|Power Supply", chassisPSRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|SEL", chassisSELRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|Storage", chassisStorageRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|System", chassisSystemHealthRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|Temperature", chassisTempRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|Volt", chassisVoltRollupStatus)
    physicalServer_obj.with_property("Hardware|Health|Memory Health", chassisSysMemPrimaryStatus)

    # BIOS
    physicalServer_obj.with_property("Settings|BIOS|Version", biosVersion)
    physicalServer_obj.with_property("Settings|BIOS|Override Enabled", biosBootSourceOverrideEnabled)
    physicalServer_obj.with_property("Settings|BIOS|Override Mode", biosBootSourceOverrideMode)
    physicalServer_obj.with_property("Settings|BIOS|Stop Boot On Fault", biosStopBootOnFault)
    physicalServer_obj.with_property("Settings|BIOS|Release Date", biosBIOSReleaseDate)

    # TPM
    physicalServer_obj.with_property("Security|TPM|Release Date", tpmFirmwareVersion)
    physicalServer_obj.with_property("Security|TPM|Interface Type", tpmInterfaceType)
    physicalServer_obj.with_metric("Security|TPM|Module Count", tpmModuleCount)
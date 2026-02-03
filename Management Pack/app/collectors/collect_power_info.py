#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven
import aria.ops.adapter_logging as logging

UNKNOWN = "unknown"
logger = logging.getLogger(__name__)

def collect_power_data(physicalServer_obj, data):
    power_supplies = data.get("PowerSupplies", [])
    voltages = data.get("Voltages", [])

    if not power_supplies:
        return

    for ps in power_supplies:
        ps_id = ps.get("@odata.id")
        ps_full_name = ps.get("Name", "PSU")
        name = ps_full_name.split(' ')[0] if ps_full_name else "PSU"

        input_ranges = ps.get("InputRanges", [])
        range_data = input_ranges[0] if isinstance(input_ranges, list) and len(input_ranges) > 0 else {}
        
        input_type = range_data.get('InputType', UNKNOWN)
        max_freq = range_data.get('MaximumFrequencyHz', 0)
        max_voltage = range_data.get('MaximumVoltage', 0)
        min_freq = range_data.get('MinimumFrequencyHz', 0)
        min_voltage = range_data.get('MinimumVoltage', 0)
        output_wattage = range_data.get('OutputWattage', 0)

        ps_status = ps.get("Status", {})
        if not isinstance(ps_status, dict): ps_status = {}
        ps_health = ps_status.get("Health", UNKNOWN)
        ps_state = ps_status.get("State", UNKNOWN)
        
        efficiency_percent = ps.get("EfficiencyPercent", 0)
        hot_pluggable = ps.get("HotPluggable", UNKNOWN)
        power_output_watts = ps.get("PowerOutputWatts", 0)
        power_input_watts = ps.get("PowerInputWatts", 0)
        last_power_output_watts = ps.get("LastPowerOutputWatts", 0)
        line_input_voltage = ps.get("LineInputVoltage", 0)
        line_input_voltage_type = ps.get("LineInputVoltageType", UNKNOWN)
        manufacturer = ps.get("Manufacturer", UNKNOWN)
        model = ps.get("Model", UNKNOWN)
        part_number = ps.get("PartNumber", UNKNOWN)
        power_capacity_watts = ps.get("PowerCapacityWatts", 0)
        power_supply_type = ps.get("PowerSupplyType", UNKNOWN)
        serial_number = ps.get("SerialNumber", UNKNOWN)

        reading_volts = 0
        voltage_health = UNKNOWN
        voltage_state = UNKNOWN

        if voltages and ps_id:
            for voltage in voltages:
                related_items = voltage.get("RelatedItem", [])
                if isinstance(related_items, list) and len(related_items) > 0:
                    related_item_id = related_items[0].get("@odata.id")
                    
                    if ps_id == related_item_id:
                        val = voltage.get("ReadingVolts")
                        reading_volts = val if val is not None else 0
                        
                        v_status = voltage.get("Status", {})
                        if isinstance(v_status, dict):
                            voltage_health = v_status.get("Health", UNKNOWN)
                            voltage_state = v_status.get("State", UNKNOWN)
                        break
        
        physicalServer_obj.with_property(f"Hardware|Power:{name}|Input Ranges|Power Input Type", input_type)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Input Ranges|Maximum Frequency", max_freq)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Input Ranges|Maximum Voltage", max_voltage)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Input Ranges|Minimum Frequency", min_freq)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Input Ranges|Minimum Voltage", min_voltage)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Input Ranges|Output Wattage", output_wattage)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS Health", ps_health)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS State", ps_state)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|PS Efficiency Percent", efficiency_percent)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS Hot Pluggable", hot_pluggable)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Power Output Watts", power_output_watts)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Power Input Watts", power_input_watts)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Last Power Output Watts", last_power_output_watts)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Line Input Voltage", line_input_voltage)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|Line Input Voltage Type", line_input_voltage_type)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS Manufacturer", manufacturer)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS Model", model)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS Part Number", part_number)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Power Capacity Watts", power_capacity_watts)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|Power Supply Type", power_supply_type)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|PS Serial Number", serial_number)
        physicalServer_obj.with_metric(f"Hardware|Power:{name}|Reading Volts", reading_volts)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|Voltage Health", voltage_health)
        physicalServer_obj.with_property(f"Hardware|Power:{name}|Voltage State", voltage_state)
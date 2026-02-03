#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

NULL_STATUS = 0
UNKNOWN = "unknown"

def collect_fan_data(physicalServer_obj, fan):
    #fanName = check_value(fan, ["Name"])

    #name = fan["Name"]
    #id = fan["Id"]
    #health = fan["Status"]["Health"]
    #state = fan["Status"]["State"]
    #hotPluggable = fan["HotPluggable"]
    #speed = fan["SpeedPercent"]["SpeedRPM"]
    #serviceLabel = fan["Location"]["PartLocation"]["ServiceLabel"]
    #fanType = fan["Oem"]["Dell"]["FanType"] > might be None type for different servers
    #pwm = fan["Oem"]["Dell"]["FanPWM"] > might be None type for different servers

    name = fan.get("Name") or UNKNOWN
    id = fan.get("Id") or UNKNOWN
    health = fan.get("Status", {}).get("Health") or UNKNOWN
    state = fan.get("Status", {}).get("State") or UNKNOWN
    hotPluggable = fan.get("HotPluggable") or UNKNOWN
    speed = fan.get("SpeedPercent", {}).get("SpeedRPM") or NULL_STATUS
    serviceLabel = fan.get("Location", {}).get("PartLocation", {}).get("ServiceLabel") or UNKNOWN
    fanType = fan.get("Oem", {}).get("Dell", {}).get("FanType") or UNKNOWN
    pwm = fan.get("Oem", {}).get("Dell", {}).get("FanPWM") or NULL_STATUS



    physicalServer_obj.with_property(f"Hardware|Cooler|Fans:{name}|ID", id)
    physicalServer_obj.with_property(f"Hardware|Cooler|Fans:{name}|Fan Health", health)
    physicalServer_obj.with_property(f"Hardware|Cooler|Fans:{name}|State", state)
    physicalServer_obj.with_property(f"Hardware|Cooler|Fans:{name}|Hot Pluggable", hotPluggable)
    physicalServer_obj.with_metric(f"Hardware|Cooler|Fans:{name}|Speed", speed)
    physicalServer_obj.with_property(f"Hardware|Cooler|Fans:{name}|Service Label", serviceLabel)
    physicalServer_obj.with_property(f"Hardware|Cooler|Fans:{name}|Fan Type", fanType)
    physicalServer_obj.with_metric(f"Hardware|Cooler|Fans:{name}|Fan PWM", pwm)



    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|ID", check_value(fan, ["Id"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|Fan Health", check_value(fan, ["Status", "Health"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|State", check_value(fan, ["Status", "State"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|Hot Pluggable", check_value(fan, ["HotPluggable"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|Speed RPM", check_value(fan, ["SpeedPercent", "SpeedRPM"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|Service Label", check_value(fan, ["Location", "PartLocation", "ServiceLabel"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|Fan Type", check_value(fan, ["Oem", "Dell", "FanType"]))
    #host_obj.with_property(f"Hardware|Cooler|Fans:{fanName}|Fan PWM", check_value(fan, ["Oem", "Dell", "FanPWM"]))
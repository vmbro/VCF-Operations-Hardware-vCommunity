#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

def check_value(data, keys, default="null"):
    try:
        for key in keys:
            data = data.get(key) if isinstance(data, dict) else None
        return data if data is not None else default
    except Exception:
        return default

def collect_fan_data(host_obj, fan):
    fanName = check_value(fan, ["Name"])
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|ID", check_value(fan, ["Id"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|Health", check_value(fan, ["Status", "Health"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|State", check_value(fan, ["Status", "State"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|Hot Pluggable", check_value(fan, ["HotPluggable"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|Speed RPM", check_value(fan, ["SpeedPercent", "SpeedRPM"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|Service Label", check_value(fan, ["Location", "PartLocation", "ServiceLabel"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|Fan Type", check_value(fan, ["Oem", "Dell", "FanType"]))
    host_obj.with_property(f"Hardware|Cooler|Fans|{fanName}|Fan PWM", check_value(fan, ["Oem", "Dell", "FanPWM"]))
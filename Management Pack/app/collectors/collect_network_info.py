#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

UNKNOWN = "unknown"

def collect_network_data(host_obj, data):
    # Push Network API info

    ipv4Address = data.get("Attributes", {}).get("CurrentIPv4.1.Address") or UNKNOWN
    dhcpEnable = data.get("Attributes", {}).get("CurrentIPv4.1.DHCPEnable") or UNKNOWN
    dns1 = data.get("Attributes", {}).get("CurrentIPv4.1.DNS1") or UNKNOWN
    dns2 = data.get("Attributes", {}).get("CurrentIPv4.1.DNS2") or UNKNOWN
    dnsFromDHCP = data.get("Attributes", {}).get("CurrentIPv4.1.DNSFromDHCP") or UNKNOWN
    ipv4Enable = data.get("Attributes", {}).get("CurrentIPv4.1.Enable") or UNKNOWN
    gateway = data.get("Attributes", {}).get("CurrentIPv4.1.Gateway") or UNKNOWN
    netmask = data.get("Attributes", {}).get("CurrentIPv4.1.Netmask") or UNKNOWN

    host_obj.with_property("Summary|Network|IPv4 Address", str(ipv4Address))
    host_obj.with_property("Summary|Network|DHCP Enable", str(dhcpEnable))
    host_obj.with_property("Summary|Network|DNS 1", str(dns1))
    host_obj.with_property("Summary|Network|DNS 2", str(dns2))
    host_obj.with_property("Summary|Network|DNS From DHCP", str(dnsFromDHCP))
    host_obj.with_property("Summary|Network|IPv4 Enable", str(ipv4Enable))
    host_obj.with_property("Summary|Network|Gateway", str(gateway))
    host_obj.with_property("Summary|Network|Netmask", str(netmask))
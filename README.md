[![Blog](https://img.shields.io/badge/Hardware%20vCommunity%20Management%20Pack-157BAD)]([https://github.com/vmbro/VCF-Operations-vCommunity-Content](https://github.com/vmbro/VCF-Operations-vCommunity-Content))
[![MP Version](https://img.shields.io/github/v/release/vmbro/VCF-Operations-Hardware-vCommunity)](https://badge.fury.io/gh/vmbro%2Fvcf-operations-hardware-vcommunity)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/vmbro/VCF-Operations-Hardware-vCommunity/total)]([https://github.com/vmbro/VCF-Operations-Hardware-vCommunity-Content](https://github.com/vmbro/VCF-Operations-Hardware-vCommunity-Content))
![GitHub repo size](https://img.shields.io/github/repo-size/vmbro/VCF-Operations-Hardware-vCommunity)
![GitHub Repo stars](https://img.shields.io/github/stars/vmbro/VCF-Operations-Hardware-vCommunity?style=flat)


# VCF Operations Hardware vCommunity
Hardware vCommunity is an open-source project that uses the Dell EMC iDRAC Redfish API to capture Dell EMC Server Metrics, Properties, and Events.  Each Adapter Instance will require the following:
* Physical Server Config File - list of Dell EMC iDRAC FQDN/IPs, one per adapter instance
* Credentials - iDRAC credentials and Dell TechDirect credentials (to capture warranty information)
* Dell iDRAC Log Monitoring Level - level of logs to collect
* Dell Warranty Checker - Enable/Disable
* Dell TechDirect URL - Dell TechDirect URL for warranty information
* Maxiumum worker threads for data collection - default is 200 maximum is 500
* Maximum worker threads for ping requests - default is 100 maximum is 100
* Adapter Mode - server monitoring or ping only
* Adapter Memory Limit (MB) - maximum amount of memory the adapter instance will use


The Hardware vCommnuity Management Pack supports Configuration Files that can have multiple FQDN/IP addresses which automatically discover these servers.  You should create a configuration file for each Adapter Instance in this format.

```xml
<IPS>
 fqdn1,
 fqdn2,
 fqdn3
</IPS>
```


## Requirements:

* Dell EMC iDRAC Credential to login and query component informations
* A configuration file that contains list of FQDN/IP addresses for integration (Configuration file name must be the same in the adapter configuration)
* Collection via Cloud Proxy

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


Management Pack supports Configuration Files that can have multiple FQDN/IP addresses and it automatically discovers these servers then creating new objects.

```
<?xml version="1.0" encoding="UTF-8"?>
<AdapterKinds>
 your-dell-server01.domain.local,
 your-dell-server02.domain.local,
 your-dell-server03.domain.local,
 your-dell-server04.domain.local,
 your-dell-server05.domain.local
</AdapterKinds>
```

Example Overview of the Hardware vCommunity Adapter

<img width="1620" height="919" alt="Screenshot 2025-06-19 at 00 06 23" src="https://github.com/user-attachments/assets/92ada679-1c85-426c-a500-7b8b0f4bd6f0" />




## Requirements:

* Credential to login iDRAC servers to query component informations
* A configuration file that contains list of FQDN/IP addresses for integration (Configuration file name must be the same in the adapter configuration)
* Datacenter name that you want to group the given server list

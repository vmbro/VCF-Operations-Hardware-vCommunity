# VCF Operations Hardware vCommunity
Hardware vCommunity is a open-source community project that uses Dell iDRAC Redfish API to group your physical servers under a datacenter name provided by user. You don't need to create multiple accounts for your servers to have an integration.

![image](https://github.com/user-attachments/assets/dccc192d-6814-4708-9284-0f65c4402de2)

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

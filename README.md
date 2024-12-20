# IP address location 通过IP地址获取地理位置

## 简介

Get geographic location through IP address, support IPv4 and IPv6. Combine IP address library and online API. The local IP address library comes from the project [lionsoul2014/ip2region](https://github.com/lionsoul2014/ip2region), and the online API comes from `ip-api` and `ip.sb`.

通过IP地址获取地理位置，支持IPv4和IPv6。结合了IP地址库和在线API。本地的IP地址库来自项目[lionsoul2014/ip2region](https://github.com/lionsoul2014/ip2region)，在线API来自`ip-api`、`ip.sb`。

## How to use 使用方法

```python
from IP2Reg import IP2Reg
ip2reg = IP2Reg()
region = ip2reg.search('8.8.8.8')
```

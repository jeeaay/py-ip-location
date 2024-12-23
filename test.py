from ipregion import IP2Region
# 可在实例化时指定ip，这时可以调用searchWithCache()、searchWithIpWhoIs()、searchWithIpApi()等方法
# You can specify the IP address when instantiating. Then you can call methods such as searchWithCache(), searchWithIpWhoIs(), searchWithIpApi(), etc.
ip2region = IP2Region("2001:4860:4860::8888")
# region = ip2region.searchWithIpApi()

region = ip2region.search('178.171.89.95')

print(region)
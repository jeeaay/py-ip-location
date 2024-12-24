from ipregion import IP2Region
# 可在实例化时指定ip，这时可以调用searchWithCache()、searchWithIpWhoIs()、searchWithIpApi()等方法
# You can specify the IP address when instantiating. Then you can call methods such as searchWithCache(), searchWithIpWhoIs(), searchWithIpApi(), etc.
# ip2region = IP2Region("2001:4860:4860::8888")
ip2region = IP2Region('178.171.89.95')

# region = ip2region.searchWithIpApi()

region = ip2region.search()

print(region)

# 实例化时指定缓存路径
# Specify the cache path when instantiating
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(cur_path, "ipcache.db3")
ip2region = IP2Region( db_path = db_path)

region = ip2region.search("2001:4860:4860::8888")
print(region)
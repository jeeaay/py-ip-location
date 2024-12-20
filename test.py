from ip2location import IP2Location
ip2location = IP2Location()
region = ip2location.search('8.8.8.8')
print(region)
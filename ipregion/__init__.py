# -*- coding=utf-8 -*-
import requests
import json, sys, os, ipaddress
from datetime import datetime, timezone, timedelta
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
from xdbSearcher import XdbSearcher
from db import Db
class IP2Region:
    def __init__(self, ip = None, db_path = None):
        self.ip = ip
        dt = datetime.now(timezone(timedelta(hours=+8)))
        self.now = dt.strftime('%Y-%m-%d %H:%M:%S')
        self.db = Db(db_path)
    def search(self, ip=None):
        if self.ip is None:
            self.ip = ip
        # 先判断是否是私有地址
        try:
            ip_obj = ipaddress.ip_address(self.ip)
        except Exception as e:
            return {'errno': 1, 'data': str(e), 'msg': 'Invalid IP address'}
        if ip_obj.is_private:
            return {'errno': 0, 'data': {"region": '私有地址 Private IP', "ip": self.ip}, 'source': 'Private IP'}
        # 使用缓存SQLite数据库搜索IP地址
        result = self.searchWithCache()
        if result['errno'] == 0:
            return result
        # 使用ipwho.is
        result = self.searchWithIpWhoIs()
        if result['errno'] == 0:
            # 存入缓存SQLite数据库
            self.db.query("INSERT INTO ip2region (ip, region, source, create_time) VALUES (?, ?, ?, ?)", args=(self.ip, result['data']['region'], result['source'], self.now))
            self.db.commit()
            return result
        # 使用ip-api搜索IP地址
        result = self.searchWithIpApi()
        if result['errno'] == 0:
            # 存入缓存SQLite数据库
            self.db.query("INSERT INTO ip2region (ip, region, source, create_time) VALUES (?, ?, ?, ?)", args=[self.ip, result['data']['region'], result['source'], self.now])
            self.db.commit()
            return result
        # 使用本地数据库搜索IP地址
        result = self.searchWithFile()
        if result['errno'] == 0:
            return result
        # 使用ip.sb搜索IP地址
        result = self.searchWithIpSb()
        if result['errno'] == 0:
            # 存入缓存SQLite数据库
            self.db.query("INSERT INTO ip2region (ip, region, source, create_time) VALUES (?, ?, ?, ?)", args=(self.ip, result['data']['region'], result['source'], self.now))
            self.db.commit()
            return result

    # description: 使用缓存SQLite数据库搜索IP地址
    # param: string ip
    # return: list
    def searchWithCache(self, ip=None):
        if self.ip is None:
            self.ip = ip
        result = self.db.query("SELECT * FROM ip2region WHERE ip = ?", (self.ip,), True)
        if result:
            return {"errno": 0, "data": {"region": result['region'], "ip": self.ip}, "source": f"Cache From {result['source']} at {result['create_time']}"}
        else:
            return {"errno": 1, "msg": "未找到IP地址"}

    # description: 使用本地数据库搜索IP地址
    # param: string ip
    # return: list
    def searchWithFile(self, ip=None):
        if self.ip is None:
            self.ip = ip
        try:
            # 创建查询对象
            dbPath = os.path.join(cur_path, "ip2region.xdb")
            searcher = XdbSearcher(dbfile=dbPath)
        except Exception as e:
            searcher.close()
            return {"errno": 3, "msg": f"本地ip数据库{dbPath}读取失败", "data": str(e)}
        try:
            # 执行查询
            region_str = searcher.searchByIPStr(self.ip)
            # 以|分割
            region_list = region_str.split('|')
            res = []
            # 忽略为0的内容，忽略重复内容
            for i in region_list:
                if i not in res and i != '' and i != '0':
                    res.append(i)
            # 拼接字符串
            region_str = ' '.join(res).strip()
            searcher.close()
            return {"errno": 0, "data": {"region": region_str, "ip": self.ip}, "source": "searchWithFile"}
        except Exception as e:
            searcher.close()
            return {"errno": 2, "msg": "本地ip数据读取失败", "data": str(e)}

    # description: 使用ip-api搜索IP地址
    # param: string ip
    # param: string lang 可选参数，默认为中文
    # return: list
    def searchWithIpApi(self, ip=None, lang="zh-CN"):
        if self.ip is None:
            self.ip = ip
        url = f"http://ip-api.com/json/{self.ip}?lang={lang}"
        try:
            response = requests.get(url)
            data = response.json()
            if data['status'] == 'success':
                country = data['country'].strip() if 'country' in set(data) != '' else ''
                region = data['regionName'].strip() if 'region' in set(data) != '' else ''
                if country == '' and region == '':
                    return {"errno": 1, "msg":"没有找到IP地址", "data": data}
                if country != region:
                    region = f"{country} {region}".strip()
                return {"errno": 0, "data": {"region": region, "ip": self.ip}, "source": "searchWithIpApi"}
            else:
                return {"errno": 1, "msg":"没有找到IP地址", "data": data}
        except Exception as e:
            return {"errno": 2, "msg":"上游服务异常", "data": str(e)}

    # description: 使用ip.sb搜索IP地址
    # param: string ip
    # return: list
    def searchWithIpSb(self, ip=None):
        if self.ip is None:
            self.ip = ip
        url = f"https://api.ip.sb/geoip/{self.ip}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            if 'code' in set(data) and data['code'] >= '400' or data['ip'] != self.ip:
                return {"errno": 1, "msg":"没有找到IP地址", "data": data}
            else:
                country = data['country'].strip() if 'country' in set(data) != '' else ''
                region = data['region'].strip() if 'region' in set(data) != '' else ''
                if country == '' and region == '':
                    return {"errno": 1, "msg":"没有找到IP地址", "data": data}
                if country != region:
                    region = f"{country} {region}".strip()
                return {"errno": 0, "data":{"region": region, "ip": self.ip}, "source": "searchWithIpSb"}
        except Exception as e:
            return {"errno": 2, "msg":"上游服务异常", "data": str(e)}

    # description: 使用ipwho.is搜索IP地址
    # param: string ip
    # param: string lang 可选参数，默认为中文
    # return: list
    def searchWithIpWhoIs(self, ip=None, lang="zh-CN"):
        if self.ip is None:
            self.ip = ip
        url = f"http://ipwho.is/{self.ip}?lang={lang}"
        try:
            response = requests.get(url)
            data = json.loads(response.text)
            if 'success' in set(data) and data['success'] == False:
                return {"errno": 1, "msg":"没有找到IP地址", "data": data}
            else:
                country = data['country'].strip() if 'country' in set(data) != '' else ''
                region = data['region'].strip() if 'region' in set(data) != '' else ''
                calling_code = data['calling_code'].strip() if 'region' in set(data) != '' else ''
                if country == '' and region == '':
                    return {"errno": 1, "msg":"没有找到IP地址", "data": data}
                if country != region:
                    region = f"{country} {region}".strip()
                if region == '':
                    return {"errno": 1, "msg":"没有找到IP地址", "data": data}
                region = f"{region} {calling_code}"
                res = []
                # 用,分割 去除重复
                for item in region.split(','):
                    if item not in res:
                        res.append(item)
                region = ','.join(res)
                return {"errno": 0, "data": {"region": region, "ip": self.ip}, "source": "searchWithIpWhoIs"}
        except Exception as e:
            return {"errno": 2, "msg":"上游服务异常", "data": str(e)}

if __name__ == "__main__":
    # 用时估算
    import time
    start_time = time.time()
    ip = IP2Region('2406:da14:2e4:8900:b5fc:b35a:34d0:93f6')
    print(ip.search())
    # 显示毫米，保留整数
    print("%d ms" % ((time.time() - start_time) * 1000))

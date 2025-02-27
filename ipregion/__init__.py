# -*- coding=utf-8 -*-
import requests
import json, sys, os, ipaddress
from datetime import datetime, timezone, timedelta
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_path)
from xdbSearcher import XdbSearcher
from db import Db
class IP2Region:
    def __init__(self, db_path = None):
        dt = datetime.now(timezone(timedelta(hours=+8)))
        self.now = dt.strftime('%Y-%m-%d %H:%M:%S')
        self.db = Db(db_path)
        # 创建查询对象
        dbPath = os.path.join(cur_path, "ip2region.xdb")
        self.searcher = XdbSearcher(dbfile=dbPath)

    def __del__(self):
        self.searcher.close()

    def search(self, ip):
        # 先判断是否是私有地址
        try:
            ip_obj = ipaddress.ip_address(ip)
        except Exception as e:
            return {'errno': 1, 'data': str(e), 'msg': 'Invalid IP address'}
        if ip_obj.is_private:
            return {'errno': 0, 'data': {"region": '私有地址 Private IP', "ip": ip}, 'source': 'Private IP'}
        # 使用缓存SQLite数据库搜索IP地址
        result = self.searchWithCache(ip)
        if result['errno'] == 0:
            return result
        # 使用本地数据库搜索IP地址
        result = self.searchWithFile(ip)
        if result['errno'] == 0:
            return result
        # 使用ipwho.is
        result = self.searchWithIpWhoIs(ip)
        if result['errno'] == 0:
            # 存入缓存SQLite数据库
            self.db.query("INSERT INTO ip2region (ip, region, source, create_time) VALUES (?, ?, ?, ?)", args=(ip, result['data']['region'], result['source'], self.now))
            self.db.commit()
            return result
        # 使用ip-api搜索IP地址
        result = self.searchWithIpApi(ip)
        if result['errno'] == 0:
            # 存入缓存SQLite数据库
            self.db.query("INSERT INTO ip2region (ip, region, source, create_time) VALUES (?, ?, ?, ?)", args=[ip, result['data']['region'], result['source'], self.now])
            self.db.commit()
            return result
        # 使用ip.sb搜索IP地址
        result = self.searchWithIpSb(ip)
        if result['errno'] == 0:
            # 存入缓存SQLite数据库
            self.db.query("INSERT INTO ip2region (ip, region, source, create_time) VALUES (?, ?, ?, ?)", args=(ip, result['data']['region'], result['source'], self.now))
            self.db.commit()
            return result

    # description: 使用缓存SQLite数据库搜索IP地址
    # param: string ip
    # return: list
    def searchWithCache(self, ip):
        result = self.db.query("SELECT * FROM ip2region WHERE ip = ?", (ip,), True)
        if result:
            return {"errno": 0, "data": {"region": result['region'], "ip": ip}, "source": f"Cache From {result['source']} at {result['create_time']}"}
        else:
            return {"errno": 1, "msg": "未找到IP地址"}

    # description: 使用本地数据库搜索IP地址
    # param: string ip
    # return: list
    def searchWithFile(self, ip):
        searcher = self.searcher
        try:
            # 执行查询
            region_str = searcher.searchByIPStr(ip)
            # 以|分割
            region_list = region_str.split('|')
            res = []
            # 忽略为0的内容，忽略重复内容
            for i in region_list:
                if i not in res and i != '' and i != '0':
                    res.append(i)
            # 拼接字符串
            region_str = ' '.join(res).strip()
            return {"errno": 0, "data": {"region": region_str, "ip": ip}, "source": "searchWithFile"}
        except Exception as e:
            return {"errno": 2, "msg": "本地ip数据读取失败", "data": str(e)}

    # description: 使用ip-api搜索IP地址
    # param: string ip
    # param: string lang 可选参数，默认为中文
    # return: list
    def searchWithIpApi(self, ip, lang="zh-CN"):
        url = f"http://ip-api.com/json/{ip}?lang={lang}"
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
                return {"errno": 0, "data": {"region": region, "ip": ip}, "source": "searchWithIpApi"}
            else:
                return {"errno": 1, "msg":"没有找到IP地址", "data": data}
        except Exception as e:
            return {"errno": 2, "msg":"上游服务异常", "data": str(e)}

    # description: 使用ip.sb搜索IP地址
    # param: string ip
    # return: list
    def searchWithIpSb(self, ip):
        url = f"https://api.ip.sb/geoip/{ip}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            if 'code' in set(data) and data['code'] >= '400' or data['ip'] != ip:
                return {"errno": 1, "msg":"没有找到IP地址", "data": data}
            else:
                country = data['country'].strip() if 'country' in set(data) != '' else ''
                region = data['region'].strip() if 'region' in set(data) != '' else ''
                if country == '' and region == '':
                    return {"errno": 1, "msg":"没有找到IP地址", "data": data}
                if country != region:
                    region = f"{country} {region}".strip()
                return {"errno": 0, "data":{"region": region, "ip": ip}, "source": "searchWithIpSb"}
        except Exception as e:
            return {"errno": 2, "msg":"上游服务异常", "data": str(e)}

    # description: 使用ipwho.is搜索IP地址
    # param: string ip
    # param: string lang 可选参数，默认为中文
    # return: list
    def searchWithIpWhoIs(self, ip, lang="zh-CN"):
        url = f"http://ipwho.is/{ip}?lang={lang}"
        try:
            response = requests.get(url)
            data = json.loads(response.text)
            if 'success' in set(data) and data['success'] == False:
                return {"errno": 1, "msg":"没有找到IP地址", "data": data}
            else:
                region = data['region'].strip() if 'region' in set(data) != '' else ''
                if region == '':
                    return {"errno": 1, "msg":"没有找到IP地址", "data": data}
                res = []
                # 用,分割 去除重复
                for item in region.split(','):
                    if item not in res:
                        res.append(item)
                region = ','.join(res)
                return {"errno": 0, "data": {"region": region, "ip": ip}, "source": "searchWithIpWhoIs"}
        except Exception as e:
            return {"errno": 2, "msg":"上游服务异常", "data": str(e)}

if __name__ == "__main__":
    # 用时估算
    import time
    start_time = time.time()
    ip = IP2Region()
    print(ip.search(ip='2406:da14:2e4:8900:b5fc:b35a:34d0:93f6'))
    # 显示毫米，保留整数
    print("%d ms" % ((time.time() - start_time) * 1000))

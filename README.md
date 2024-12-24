# IP address location 通过IP地址获取地理位置

## Introduction 简介

Get geographic location through IP address, support IPv4 and IPv6. Combine IP address library and online API. The local IP address library comes from the project [lionsoul2014/ip2region](https://github.com/lionsoul2014/ip2region), and the online API comes from `ipwho.is`, `ip-api` and `ip.sb`.

通过IP地址获取地理位置，支持IPv4和IPv6。结合了IP地址库和在线API。本地的IP地址库来自项目[lionsoul2014/ip2region](https://github.com/lionsoul2014/ip2region)，在线API来自`ipwho.is`、`ip-api`、`ip.sb`。

Pypi: [ipregion](https://pypi.org/project/ip-region/)

## How to use 使用方法

Install 安装：

```bash
pip install ip-region
```

Use 使用：

```python
from ipregion import IP2Region
ip2region = IP2Region()
region = ip2region.search('8.8.8.8')
```

## Caching Data 缓存数据

By default, after calling the online API, it will be cached in `ipcache.db3` under this project. If you want to persist the cache data, you can pass in the cache file path when instantiating it, for example:

默认情况下，调用在线API后将会缓存在本项目下的`ipcache.db3`里，如果想要持久保存缓存数据，可以在实例化时传入缓存文件路径，例如：

```python
# 实例化时指定缓存路径
# Specify the cache path when instantiating
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(cur_path, "ipcache.db3")
ip2region = IP2Region( db_path = db_path)
region = ip2region.search("2001:4860:4860::8888")
````

> The first time you specify the cache path, the target database file will be generated, so it will be a little slower
>
> 第一次指定缓存路径后，会生成目标数据库文件，所以会慢一点

## Use in Flask 结合Flask使用

Example file 示例文件:   `example1_flask.py`

> View it on github 请在github上查看
>
> [example1_flask.py](https://github.com/jeeaay/py-ip-location/blob/main/example1_flask.py)

insstall Flask 安装Flask:

```bash
pip install flask
```

run 运行:
```bash
python example1_flask.py
```

visit 访问本地测试路径:
```
http://127.0.0.1:5000/ip/<search ip>
```

API:
```bash
# 获取IP对应位置
GET http://127.0.0.1:5000/ip/8.8.8.8
# 获取IPv6对应位置
GET http://127.0.0.1:5000/ip/2406:da14:2e4:8900:b5fc:b35a:34d0:93f6
### 获取IP对应位置, 使用jsonp, callbackFunction可以自定义
GET http://127.0.0.1:5000/ip/8.8.8.8?callback=callbackFunction
```

Example code 示例代码:

```python
from flask import Flask, jsonify, request
from ipregion import IP2Region
import json
app = Flask(__name__)
@app.route("/ip/<ip>")
def get_ip(ip=None):
    ip2region = IP2Region()
    region = ip2region.search(ip)
    # json
    if not request.args.get('callback') or request.args.get('callback').strip() == '':
        return jsonify(region)
    # jsonp
    else:
        return request.args.get('callback') + "(" + json.dumps(region) + ")"
if __name__ == "__main__":
    app.run(debug=True)
```

## LICENSE

Apache-2.0 License

## Source code

https://github.com/jeeaay/py-ip-location

## Upload to pypi

install twine and build

```bash
pip install twine build
```

build

```bash
python -m build
```

upload

```bash
twine upload dist/*
```

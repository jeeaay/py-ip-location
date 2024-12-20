# IP address location 通过IP地址获取地理位置

## 简介

Get geographic location through IP address, support IPv4 and IPv6. Combine IP address library and online API. The local IP address library comes from the project [lionsoul2014/ip2region](https://github.com/lionsoul2014/ip2region), and the online API comes from `ip-api` and `ip.sb`.

通过IP地址获取地理位置，支持IPv4和IPv6。结合了IP地址库和在线API。本地的IP地址库来自项目[lionsoul2014/ip2region](https://github.com/lionsoul2014/ip2region)，在线API来自`ip-api`、`ip.sb`。

## How to use 使用方法

```python
from ip2location import IP2Location
ip2location = IP2Location()
region = ip2location.search('8.8.8.8')
```

## Use in Flask 结合Flask使用

Example file 示例文件:   `example1_flask.py`

Example API documentation 示例的API文档： `api.http`

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

```python
from flask import Flask, jsonify, request
from ip2location import IP2Location
import json
app = Flask(__name__)
@app.route("/ip/<ip>")
def get_ip(ip=None):
    # json
    if not request.args.get('callback') or request.args.get('callback').strip() == '':
        return jsonify(IP2Location(ip).search())
    # jsonp
    else:
        return request.args.get('callback') + "(" + json.dumps(IP2Location(ip).search()) + ")"
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
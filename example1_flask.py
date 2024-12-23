from flask import Flask, jsonify, request
from ipregion import IP2Region
import json

# insstall flask:   pip install flask
# run:              python example1_flask.py
# visit:            http://127.0.0.1:5000/ip/<search ip>

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

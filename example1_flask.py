from flask import Flask, jsonify, request
from IP2Reg import IP2Reg
import json

# pip install flask

app = Flask(__name__)

@app.route("/")
def home():
    return f"<p>Hello, World!</p>"

@app.route("/ip/<ip>")
def get_ip(ip=None):
    # jsonp情况
    if not request.args.get('callback') or request.args.get('callback').strip() == '':
        return jsonify(IP2Reg(ip).search())
    else:
        print(request.args.get('callback') + json.dumps(IP2Reg(ip).search()))
        return request.args.get('callback') + "(" + json.dumps(IP2Reg(ip).search()) + ")"

if __name__ == "__main__":
    # searchWithFile('8.8.8.8')
    app.run(debug=True)

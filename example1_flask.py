from flask import Flask, jsonify, request
from IP2Reg import IP2Reg
import json

# insstall flask:   pip install flask
# run:              python example1_flask.py
# visit:            http://127.0.0.1:5000/ip/<search ip>

app = Flask(__name__)

@app.route("/")
def home():
    return f"<p>Hello, World!</p>"


@app.route("/ip/<ip>")
def get_ip(ip=None):
    # json
    if not request.args.get('callback') or request.args.get('callback').strip() == '':
        return jsonify(IP2Reg(ip).search())
    # jsonp
    else:
        return request.args.get('callback') + "(" + json.dumps(IP2Reg(ip).search()) + ")"

if __name__ == "__main__":
    # searchWithFile('8.8.8.8')
    app.run(debug=True)

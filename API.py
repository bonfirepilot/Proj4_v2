import os
from math import sqrt
from flask import Flask, escape, request, jsonify
from urllib import request, parse
import hashlib
from redis import Redis, RedisError
from requests import *
import json
import os
import requests

redis = Redis(host="redis", socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
#redis = Redis(host="redis", socket_connect_timeout=2, socket_timeout=2)

@app.route('/')
def root():
    return "Hello There General Kenobi!"

def Fact1(n: int):
    fact = 1
    if n < 0:
        return False
    elif n == 0:
        return 1
    else:
        for i in range(1, n + 1):
            fact = fact*i
        return fact
@app.route("/factorial/<int:n>")
def send_Fact1(n):
    output = {
        "input": n,
        "output": int(Fact1(n))
    }
    return json.dumps(output)
@app.route('/md5/<val>')
def md5_str(val: str):
    m = hashlib.md5()
    m.update(val.encode('utf8'))

    output = {
        "input": val,
        "output": m.hexdigest()
    }
    return json.dumps(output)
@app.route("/fibonacci/<int:n>")
def fibo_send(n: int):
    def fibo(n):
        a, b = 0, 1
        array = [0]
        while b <= n:
            array.append(b)
            a, b = b, a+b
        return array
        for i in range(0, len(array)):
            array[i] = str(array[i])
    output = {
        "input": n, 
        "output": (fibo(n))
    }
    return json.dumps(output)
def prime(n: int):
    if n > 1:
        for i in range(2,n):
            if (n % i) == 0:
                return False
        else:
            return True
    if n == 1:
        return False
@app.route("/is-prime/<int:n>")
def send_prime(n):
    output = {
        "input": n, 
        "output": (prime(n))
    }
    return json.dumps(output)
@app.route("/slack-alert/<text>")
def send_message_to_slack(text: str):

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))
    output = {
        "input": text,
        "output": True
    }
    return json.dumps(output)
    send_message_to_slack("<text>")
@app.route('/keyval/', methods = ["POST", "PUT"])
def record():
	try:
		data = request.json
		key, value = data.items()[0]

		if request.method == "POST":
			if db.exists(key):
				return json.dumps({"input": "new-key", "output": False, "error": "Unable to add pair: key already exists."})
			else:
				db.set(key, value)
				return json.dumps({"input": "new-key", "output": True})

		elif request.method == "PUT":
			if db.exists(key):
				db.set(key, value)
				return json.dumps({"input": "existing-key", "output": True})
			else:
				return json.dumps({"input": "existing-key", "output": False, "error": "Unable to update value: key does not exist."})
				
		else:
			raise
	except Exception as err:
		return json.dumps({"output": False, "error": err})
		

@app.route('/keyval/<string:key>')
def retrieve(key):
	try:
		if db.exists(key):
			return json.dumps({"input": "retrieve-value", "output": db.get(key)})
		else:
			return json.dumps({"input": "retrieve-value", "output": False, "error": "Unable to update value: key does not exist."})
			
	except Exception as err:
		return json.dumps({"output": False, "error": err})




if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)

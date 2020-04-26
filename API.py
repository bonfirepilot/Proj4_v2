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

@app.route('/keyval', methods=['POST', 'PUT'])
def kv_upsert():
    
    _JSON = {
        'key': None,
        'value': None,
        'command': 'CREATE' if request.method=='POST' else 'UPDATE',
        'result': False,
        'error': None
    }

    
    try:
        payload = request.get_json()
        _JSON['key'] = payload['key']
        _JSON['value'] = payload['value']
        _JSON['command'] += f" {payload['key']}/{payload['value']}"
    except:
        _JSON['error'] = "Missing or malformed JSON in client request."
        return jsonify(_JSON), 400

   
    try:
        test_value = redis.get(_JSON['key'])
    except RedisError:
        _JSON['error'] = "Cannot connect to redis."
        return jsonify(_JSON), 400

    
    if request.method == 'POST' and not test_value == None:
        _JSON['error'] = "Cannot create new record: key already exists."
        return jsonify(_JSON), 409

   
    else if request.method == 'PUT' and test_value == None:
        _JSON['error'] = "Cannot update record: key does not exist."
        return jsonify(_JSON), 404

    else:
        if redis.set(_JSON['key'], _JSON['value']) == False:
            _JSON['error'] = "There was a problem creating the value in Redis."
            return jsonify(_JSON), 400
        else:
            _JSON['result'] = True
            return jsonify(_JSON), 200


@app.route('/keyval/<string:key>', methods=['GET', 'DELETE'])
def kv_retrieve(key):
   
    _JSON = {
        'key': key,
        'value': None,
        'command': "{} {}".format('RETRIEVE' if response.method=='GET' else 'DELETE', key)
        'result': False,
        'error': None
    }

    
    try:
        test_value = redis.get(key)
    except RedisError:
        _JSON['error'] = "Cannot connect to redis."
        return jsonify(_JSON), 400

    if test_value == None:
        _JSON['error'] = "Key does not exist."
        return jsonify(_JSON), 404
    else:
        _JSON['value'] = test_value

    # GET == retrieve
    if response.method == 'GET':
        _JSON['result'] = True
        return jsonify(_JSON), 200

   
    else if response.method == 'DELETE':
        ret = redis.delete(key)
        if ret == 1:
            _JSON['result'] = True
            return jsonify(_JSON)
        else:
            _JSON['error'] = f"Unable to delete key (expected return value 1; client returned {ret})"
            return jsonify(_JSON), 400





if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)

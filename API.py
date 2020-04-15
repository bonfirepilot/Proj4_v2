from flask import Flask, escape, request, jsonify
from urllib import request, parse
import hashlib
import json
import os


app = Flask(__name__)

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
        if n < 1:
            return 0
        elif n == 1:
            return 1
        else:
            return fibo(n-1)+fibo(n-2)
    fib_list = []
    for iter in range(int(n)):
        fib_list.append(fibo(iter))
    global fib_print
    fib_print = []
    for k in fib_list:
        fib_print.append(int(k))
    output = {
        "input": n, 
        "output": fib_print
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
        return True
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



if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)

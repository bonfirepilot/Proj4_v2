from flask import Flask, escape, request
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
        return("Sorry, Factorial does not exist")
    elif n == 0:
        return("The factorial of 0 is 1")
    else:
        for i in range(1, n + 1):
            fact = fact*i
        return("The factorial of",n,"is",fact)
@app.route("/factorial/<int:n>")
def send_Fact1(n):
    output = {
        "input": n,
        "output": str(Fact1(n))
    }
    return json.dumps(output)
@app.route("/factorial/<n>")
def not_Fact1(n):
    output = {
        "input": n,
        "output": "This is not a number"
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

# The Fibonacci function
def fibo(n: int):
    """
    Calculating the fibonacci numbers
    """
    if n < 1:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo(n-1)+fibo(n-2)

# The actual route
@app.route("/fibonacci/<int:n>")
def send_fibo(n):
    """
    Sending the fibonacci number to the user, telling him if
    he uses improper input
    """
    output = {
        "input": n, 
        "output": str(fibo(n))
    }
    return json.dumps(output)
@app.route("/fibonacci/<n>")
def not_fibo(n):
    output = {
        "input": n,
        "output": "This is not a number"
    }
    return json.dumps(output)
def prime(n: int):
    if n > 1:
       for i in range(2, n//2):
          if(n % i) == 0:
             return(n, "is not a prime number")
       else:
         return(n, "is a prime number")
    else:
      return(n, "is not a prime number")
@app.route("/is-prime/<int:n>")
def send_prime(n):
    output = {
        "input": n, 
        "output": str(prime(n))
    }
    return json.dumps(output)
@app.route("/is-prime/<n>")
def not_prime(n):
    output = {
        "input": n,
        "output": "this is not a number"
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
        "output": "sent message"
    }
    return json.dumps(output)
    send_message_to_slack("<text>")



if __name__ == '__main__':
    app.run(debug=True)

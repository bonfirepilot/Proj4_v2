from flask import Flask, escape, request
import hashlib
import json

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
@app.route("/factorial")
def send_Fact1():
    try:
        return str(Fact1(int(request.args['n'])))
    except ValueError:
        return "Please use a positive number"
 
@app.route('/md5')
def md5_str():
    val = request.args.get("str")
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
@app.route("/fibonacci")
def send_fibo():
    """
    Sending the fibonacci number to the user, telling him if
    he uses improper input
    """
    try:
        return str(fibo(int(request.args['n'])))
    except ValueError:
        return "Please use a number as the 'n' argument"
def prime(n: int):
    if n > 1:
       for i in range(2, n//2):
          if(n % i) == 0:
             return(n, "is not a prime number")
             break
       else:
         return(n, "is a prime number")
    else:
      return(n, "is not a prime number")
@app.route("/is-prime")
def send_prime():
    try:
        return str(prime(int(request.args['n'])))
    except ValueError:
        return "not a prime number"
if __name__ == '__main__':
    app.run(debug=True)

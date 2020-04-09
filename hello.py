from flask import Flask
import hashlib
import json

app = Flask(__name__)

@app.route('/')
def root():
    return "Hello, World!"

@app.route('/factorial')
def hello():
    factorial = request.args.get('arg')
    fact = 1
    if factorial < 0:
        print("Sorry, Factorial does not exist")
    elif factorial == 0:
        print("The factorial of 0 is 1")
    else:
        for i in range(1, factorial + 1):
            fact = fact*1
        print("The factorial of",factorial,"is",fact)
 

 #This is for the Is Prime section of the project
@app.route('/isprime/<num>')
def is_prime(num):
    if num < 2:
        return 'Enter number larger than 1'
    else:
        for x in range(2,num):
            if num % x == 0:
               return 'Not prime'
        return 'Is prime'
    #returns Is Prime 

    
if __name__ == "__main__":
    app.debug = True 
    app.run('0.0.0.0')

    #return f'Hello, {escape(name)}!'
    return 'factorial'
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
if __name__ == '__main__':
    app.run(debug=True)

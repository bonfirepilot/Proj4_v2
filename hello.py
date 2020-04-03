from flask import Flask, escape, request
import hashlib
import json

app = Flask(__name__)

@app.route('/')
def root():
    return "Hello There General Kenobi!"

@app.route('/factorial')
def hello():
    num = int(input(request.args.get('arg1')))
    fact = 1
    if num < 0:
        print("Sorry, Factorial does not exist")
    elif num == 0:
        print("The factorial of 0 is 1")
    else:
        for i in range(1, num + 1):
            fact = fact*i
    print("The factorial of",num,"is",fact)
    output1 = {
        "input": num,
        "output": print
    }

    #return f'Hello, {escape(name)}!'
    return json.dumps(output1) 
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

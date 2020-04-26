@app.route('/kv-record/', methods = ["POST", "PUT"])
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
		

@app.route('/kv-retrieve/<string:key>')
def retrieve(key):
	try:
		if db.exists(key):
			return json.dumps({"input": "retrieve-value", "output": db.get(key)})
		else:
			return json.dumps({"input": "retrieve-value", "output": False, "error": "Unable to update value: key does not exist."})
			
	except Exception as err:
		return json.dumps({"output": False, "error": err})


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

    # Can't retrieve OR delete if the value doesn't exist
    if test_value == None:
        _JSON['error'] = "Key does not exist."
        return jsonify(_JSON), 404
    else:
        _JSON['value'] = test_value

    # GET == retrieve
    if response.method == 'GET':
        _JSON['result'] = True
        return jsonify(_JSON), 200

    # DELETE == delete (duh)
    else if response.method == 'DELETE':
        ret = redis.delete(key)
        if ret == 1:
            _JSON['result'] = True
            return jsonify(_JSON)
        else:
            _JSON['error'] = f"Unable to delete key (expected return value 1; client returned {ret})"
            return jsonify(_JSON), 400

@app.route('/slack-alert/<string:msg>')
def post_to_slack(msg):
    data = { 'text': msg }
    resp = requests.post(SLACK_URL, json=data)
    if resp.status_code == 200:
        result = True
        mesg = "Message successfully posted to Slack channel " + SLACK_CHANNEL
    else:
        result = False
        mesg = "There was a problem posting to the Slack channel (HTTP response: " + str(resp.status_code) + ")."

    return jsonify(
        input=msg,
        message=mesg,
        output=result
    ), 200 if resp.status_code== 200 else 400

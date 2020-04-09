import requests
import json
web_hook_url = 'Have the webhook saved on my computer and will put it in later'

x = 6

slack_msg = {'text': x }

requests.post(web_hook_url,data=json.dumps(slack_msg))

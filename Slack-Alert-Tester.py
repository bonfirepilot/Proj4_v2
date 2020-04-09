import requests
import json
web_hook_url = 'https://hooks.slack.com/services/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'

x = 6

slack_msg = {'text': x }

requests.post(web_hook_url,data=json.dumps(slack_msg))

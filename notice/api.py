import requests
import json
import time
import hmac
import hashlib
import base64
import urllib

def dingding(title: str, text: str, token: str, secret: str):
    timestamp = int(round(time.time() * 1000))
    secret_enc = bytes(secret, encoding='utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign, encoding='utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(token, timestamp, sign)
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "{}".format(title),
            "text": "{}".format(text)
        }
    }
    try:
        requests.post(url=url, data=json.dumps(data), headers=headers)
    except Exception:
        pass

def wechat(title: str, text: str, sckey: str):
    url = 'https://sc.ftqq.com/{}.send'.format(sckey)
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": "{}".format(title),
        "desp": "{}".format(text)
    }
    try: 
        requests.post(url=url, data=data, headers=headers)
    except Exception:
        pass
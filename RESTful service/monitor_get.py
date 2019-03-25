#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import base64
import hmac
import hashlib
import urllib
import time
import requests

reload(sys)
sys.setdefaultencoding("utf8")

'''
This demo shows how to use the RESTful API to upload an audio file ( "data_type":"audio" ) into your bucket.
You can find account_access_key and account_access_secret in your account page.
Log into http://console.acrcloud.com -> "Account" (top right corner) -> "RESTful API Keys" -> "Create Key Pair".
Be Careful, they are different with access_key and access_secret of your project.
'''
account_access_key = "###YOUR_ACCESS_KEY###"
account_access_secret = "###YOUR_ACCESS_SECRET###"

requrl = "https://api.acrcloud.com/v1/monitor-streams"
http_method = "GET"
http_uri = "/v1/monitor-streams"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+account_access_key+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(
        hmac.new(account_access_secret, string_to_sign, digestmod=hashlib.sha1)
        .digest())

headers = {'access-key': account_access_key, 'signature-version': signature_version, 'signature': sign, 'timestamp':str(timestamp)}
params = {'project_name':"monitor_test"}

r = requests.get(requrl, params=params, headers=headers, verify=True)
r.encoding = "utf-8"
print r.text

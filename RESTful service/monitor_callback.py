import sys
import os
import base64
import hmac
import hashlib
import urllib
import time
import requests

'''
This demo shows how to use the RESTful API to upload an audio file ( "data_type":"audio" ) into your bucket.
You can find account_access_key and account_access_secret in your account page.
Log into http://console.acrcloud.com -> "Account" (top right corner) -> "RESTful API Keys" -> "Create Key Pair".
Be Careful, they are different with access_key and access_secret of your project.
'''
account_access_key = "account_access_key"
account_access_secret = "account_secret_key"

#replace "your_project_key" with your monitor project key
requrl = "https://api.acrcloud.com/v1/monitors/your_project_key/callback"
http_method = "POST"
http_uri = "/v1/monitors/your_project_key/callback"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+account_access_key+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(
        hmac.new(account_access_secret, string_to_sign, digestmod=hashlib.sha1)
        .digest())

headers = {'access-key': account_access_key, 'signature-version': signature_version, 'signature': sign, 'timestamp':timestamp}
data = {'callback_url':'http://www.your_url.com', 'post_type':'json', 'send_noresult':0}

r = requests.post(requrl, data=data, headers=headers, verify=True)
r.encoding = "utf-8"
print r.text

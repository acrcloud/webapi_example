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
account_access_key = "xxxxxx"
account_access_secret = "xxxxxx"

requrl = "https://api.acrcloud.com/v1/monitors/2104"
http_method = "PUT"
http_uri = "/v1/monitors/2104"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+account_access_key+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(
        hmac.new(account_access_secret, string_to_sign, digestmod=hashlib.sha1)
        .digest())

headers = {'access-key': account_access_key, 'signature-version': signature_version, 'signature': sign, 'timestamp':timestamp}
data = {'url':'http://rs.ajmide.com/r_11/11.m3u8', 'stream_name':'test_cn', "region":"ap-northeast-1"}

r = requests.put(requrl, data=data, headers=headers, verify=True)
r.encoding = "utf-8"
print r.text

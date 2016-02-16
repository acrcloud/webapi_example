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
Log into http://console.acrcloud.com -> "Your Name"(top right corner) -> "Account" -> "Console API Keys" -> "Create Key Pair". 
Be Careful, they are different with access_key and access_secret of your project.
'''
account_access_key = "xxxxxxxx"
account_access_secret = "xxxxxxxx"

requrl = "https://api.acrcloud.com/v1/audios"
http_method = "POST"
http_uri = "/v1/audios"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+account_access_key+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(
        hmac.new(account_access_secret, string_to_sign, digestmod=hashlib.sha1)
        .digest())

f = open(sys.argv[1], "r")

files = {'audio_file':f}
headers = {'access-key': account_access_key, 'signature-version': signature_version, 'signature': sign, 'timestamp':timestamp}
#if you uplaod fingerprint file , please set "data_type":"fingerprint"
data = {'title':"api_test", "audio_id":1234, "bucket_name":"test", "data_type":"audio", "custom_key[0]":"key1", "custom_value[0]":"key2"}

r = requests.post(requrl, files=files, data=data, headers=headers, verify=True)
r.encoding = "utf-8"
print r.text

import sys
import os
import urllib
import urllib2
import base64
import hmac
import hashlib
import time

access_key = "xxxxxx"
access_secret = "xxxxxx"

# suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc
# File size: < 1M , You'de better cut large file to small file, within 15 seconds data size is better
f = open(sys.argv[1], "r")
sample_bytes = os.path.getsize(sys.argv[1])
content = f.read()
f.close()

http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"
timestamp = time.time()

string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)

sign = base64.b64encode(hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1).digest())
test_data = {'access_key':access_key,
            'sample_bytes':sample_bytes,
            'sample':base64.b64encode(content),
            'timestamp':str(timestamp),
            'signature':sign,
            'data_type':data_type,
            "signature_version":signature_version}

test_data_urlencode = urllib.urlencode(test_data)

requrl = "http://ap-southeast-1.api.acrcloud.com/v1/identify"

req = urllib2.Request(url = requrl,data =test_data_urlencode)

res_data = urllib2.urlopen(req)
res = res_data.read()
print res

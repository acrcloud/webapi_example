'''
This is a demo program which implements ACRCloud Identify Protocol V1 all by native python libraries.
'''

import sys
import os
import base64
import hmac
import hashlib
import time
import httplib
import mimetools

def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files):
    boundary = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields.items():
        L.append('--' + boundary)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(str(value))
    for (key, value) in files.items():
        L.append('--' + boundary)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, key))
        L.append('Content-Type: application/octet-stream')
        L.append('')
        L.append(value)
    L.append('--' + boundary + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body

'''
Replace "xxxxxxxx" below with your project's access_key and access_secret.
'''
access_key = "xxxxxxxx"
access_secret = "xxxxxxxx"

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

fields = {'access_key':access_key,
          'sample_bytes':sample_bytes,
          'timestamp':str(timestamp),
          'signature':sign,
          'data_type':data_type,
          "signature_version":signature_version}

res = post_multipart("ap-southeast-1.api.acrcloud.com", "/v1/identify", fields, {"sample":content})
print res

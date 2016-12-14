import sys
import os
import base64
import hmac
import hashlib
import urllib
import time
import requests

option = {
  'host': 'api.acrcloud.com',
  'signature_version': '1',
  'access_key': '<your account access key>', 
  'access_secret': '<your account access secret>'
};


def sign(string_to_sign, access_secret):
    return  base64.b64encode(
		    hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1)
		    .digest())
	
def create_bucket(name, type, scale, content_type):
    http_method = "POST"
    timestamp = time.time()
    uri = '/v1/buckets'
    
    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])
 
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'name':name, 'type':type, 'scale':scale,'content_type':content_type}
    
    requrl = "https://"+option['host'] + uri
    r = requests.post(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def delete_bucket(name):
    http_method = "DELETE"
    timestamp = time.time()
    uri = '/v1/buckets'+"/"+name
    
    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])
 
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'name':name}
    
    requrl = "https://"+option['host'] + uri
    r = requests.delete(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text
def list_buckets():
    http_method = "GET"
    timestamp = time.time()
    uri = '/v1/buckets'

    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + uri 
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

if __name__ == "__main__":
    create_bucket('test_api_bucket', 'File', 100, "Music")
    #list_buckets()
    #delete_bucket('test_api_bucket')

import sys
import os
import base64
import hmac
import hashlib
import urllib
import time
import requests
import json

option = {
  'host': 'api.acrcloud.com',
  'signature_version': '1',
  'access_key': '<your account access key>',
  'access_secret': '<your account access secret>'
};


def sign(string_to_sign, access_secret):
    return  base64.b64encode(
		    hmac.new(access_secret.encode(), string_to_sign.encode(), digestmod=hashlib.sha1)
		    .digest())
	
def create_offline(name, buckets, audio_type, region):
    http_method = "POST"
    timestamp = str(time.time())
    uri = '/v1/offlinedbs'
    
    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])
 
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'name':name, 'buckets':json.dumps(buckets), 'audio_type':audio_type, 'region':region}
    
    requrl = "https://"+option['host'] + uri
    r = requests.post(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text
	
def rebuild_offline(name, buckets = None):
    http_method = "PUT"
    timestamp = time.time()
    uri = '/v1/offlinedbs/'+name
    
    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])
 
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + uri
    if buckets:
        data = {'buckets':json.dumps(buckets)}
        r = requests.put(requrl, headers=headers, data=data, verify=True)
        r.encoding = "utf-8"
        print r.text
    else:
        r = requests.put(requrl, headers=headers, verify=True)
        r.encoding = "utf-8"
        print r.text

def delete_offline(name):
    http_method = "DELETE"
    timestamp = str(time.time())
    uri = '/v1/offlinedbs'+"/"+name
    
    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])
 
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + uri
    r = requests.delete(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_offline(name, path):
    http_method = "GET"
    timestamp = str(time.time())
    uri = '/v1/offlinedbs'+"/"+name

    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}
    requrl = "https://"+option['host'] + uri
    r = requests.get(requrl, headers=headers, verify=True)
    if r.status_code == 200:
        f = open(path, 'wb')
        f.write(r.content)
        f.close()

def rebuild_offline_with_files(name, file_list):
    http_method = "PUT"
    timestamp = str(time.time())
    uri = '/v1/offlinedbs/'+name

    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], timestamp))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + uri
    data = {'files':file_list}
    r = requests.put(requrl, headers=headers, json=data, verify=True)
    r.encoding = "utf-8"
    print r.text

if __name__ == "__main__":
    create_offline('test_api_offline_project', [{"name":"offline-bucket", "id":333}], 1, "eu-west-1")
    #rebuild_offline('test_api_offline_project')
    #rebuild_offline('test_api_offline_project', [{"name":"offline-bucket", "id":333}])
    #delete_offline('test_api_offline_project')
    #get_offline("test_api_offline_project", "./acrcloud_local_db.zip")
    #rebuild_offline_with_files("test_api_offline_project", ["c738810677f746de3d3800f7f95b9f64"])

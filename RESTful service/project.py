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
  'access_secret': '<your account access secret>',
};


def sign(string_to_sign, access_secret):
    return  base64.b64encode(
		    hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1)
		    .digest())

def create_project(name, region, type, buckets, audio_type, external_id):
    http_method = "POST"
    timestamp = time.time()
    uri = '/v1/projects'
    
    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])
 
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'name':name, 'region':region, 'type':type, 'buckets':buckets, 'audio_type':audio_type, 'external_id':external_id}
    
    requrl = "https://"+option['host'] + uri
    r = requests.post(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text


def update_project(name, buckets):
    http_method = "PUT"
    timestamp = time.time()
    uri = '/v1/projects/'+name

    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'buckets':buckets}

    requrl = "https://"+option['host'] + uri
    r = requests.put(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def delete_project(name):
    http_method = "DELETE"
    timestamp = time.time()
    uri = '/v1/projects'+"/"+name

    string_to_sign = '\n'.join((http_method, uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'name':name}

    requrl = "https://"+option['host'] + uri
    r = requests.delete(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_project(project_name):
    http_method = "GET"
    timestamp = time.time()
    http_uri = "/v1/projects/"+project_name

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def list_projects():
    http_method = "GET"
    timestamp = time.time()
    http_uri = "/v1/projects"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text


if __name__ == "__main__":
    create_project('test_api_project', 'us-west-2', 'AVR', "test_api_bucket", 1, "")
    get_project('test_api_project')
    update_project('test_api_project', "ACRCloud Music")
    delete_project('test_api_project')
    list_projects()

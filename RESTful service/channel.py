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
option = {
  'host': 'api.acrcloud.com',
  'signature_version': '1',
  'access_key': 'your console access key',
  'access_secret': 'your console access scret',
};


def sign(string_to_sign, access_secret):
    return  base64.b64encode(
		    hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1)
		    .digest())

def create_channel(bucket, channel_url, title, channel_id, custom_fields=None):
    http_method = "POST"
    timestamp = time.time()
    http_uri = "/v1/channels"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}
    data = {'url':channel_url,'title':title, "channel_id":channel_id, "bucket_name":bucket}
    if custom_fields:
        keys = []
        values = []
        for k in custom_fields:
            keys.append(k)
            values.append(custom_fields[k])
        data['custom_key[]'] = keys
        data['custom_value[]'] = values

    requrl = "https://"+option['host'] + http_uri
    r = requests.post(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_all_channels(bucket, page=1):
    http_method = "GET"
    timestamp = time.time()
    http_uri = "/v1/buckets/"+bucket+"/channels"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri+"?page="+str(page)
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_channel(acr_id):
    http_method = "GET"
    timestamp = time.time()
    http_uri = "/v1/channels/"+acr_id

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def delete_channel(acr_id):
    http_method = "DELETE"
    timestamp = time.time()
    http_uri = "/v1/channels/"+acr_id

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.delete(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    if r.status_code == 204:
        print "deleted"

if __name__ == "__main__":
    #create_channel('eu_test', 'http://127.0.0.1', 'channel 1', '12345')
    delete_channel("722ad0163be810eb972c1f619aa1f1b3")
    #get_all_channels('eu_test', 1)
    #get_channel('b6c9985babb2e9ecb1642d04a7b149d8')

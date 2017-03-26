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
  'access_key': 'your_account_access_key(not project key)',
  'access_secret': 'your_account_access_secret'
};


def sign(string_to_sign, access_secret):
    return  base64.b64encode(
		    hmac.new(access_secret, string_to_sign, digestmod=hashlib.sha1)
		    .digest())

def create_channel_playback(bucket_id, channel_id, time_length):
    http_method = "POST"
    timestamp = time.time()
    http_uri = "/v1/channel-playback"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}
    data = {"bucket_id":bucket_id, "channel_id":channel_id, "time":int(time_length)}

    requrl = "https://"+option['host'] + http_uri
    r = requests.post(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def update_channel_playback(id, bucket_id, channel_id, time_length):
    http_method = "PUT"
    timestamp = time.time()
    http_uri = "/v1/channel-playback/"+str(id)

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}
    data = {"bucket_id":bucket_id, "channel_id":channel_id, "time":int(time_length)}

    requrl = "https://"+option['host'] + http_uri
    r = requests.put(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_all_channel_playback(bucket_id, page=1):
    http_method = "GET"
    timestamp = time.time()
    http_uri = "/v1/buckets/"+str(bucket_id)+"/channel-playback"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri+"?page="+str(page)
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_channel_playback(id):
    http_method = "GET"
    timestamp = time.time()
    http_uri = "/v1/channel-playback/"+str(id)

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def delete_channel_playback(id):
    http_method = "DELETE"
    timestamp = time.time()
    http_uri = "/v1/channel-playback/"+str(id)

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.delete(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    if r.status_code == 204:
        print "deleted"

if __name__ == "__main__":
    timestamp = time.time()
    create_channel_playback(3833, 666, 7*24*3600)
    #update_channel_playback(1, 3833, 666, 30*24*3600);
    #get_all_channel_playback(3833)
    #get_channel_playback(1)
    #delete_channel_playback(1)

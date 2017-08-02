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
  'access_key': '<account_access_key>',
  'access_secret': '<account_access_scret>',
};


def sign(string_to_sign, access_secret):
    return  base64.b64encode(
		    hmac.new(access_secret.encode(), string_to_sign.encode(), digestmod=hashlib.sha1)
		    .digest())

def upload_audio(path, bucket, title, audio_id, data_type="audio", custom_fields=None):
    http_method = "POST"
    timestamp = str(time.time())
    http_uri = "/v1/audios"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))

    signature = sign(string_to_sign, option['access_secret'])

    f = open(path, "rb")

    files = {'audio_file':f}
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}
    #if you uplaod fingerprint file , please set "data_type":"fingerprint"
    data = {'title':title, "audio_id":audio_id, "bucket_name":bucket, "data_type":data_type}
    if custom_fields:
        keys = []
        values = []
        for k in custom_fields:
            keys.append(k)
            values.append(custom_fields[k])
        data['custom_key[]'] = keys
        data['custom_value[]'] = values

    requrl = "https://"+option['host'] + http_uri
    r = requests.post(requrl, files=files, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def get_audios(bucket, page=1):
    http_method = "GET"
    timestamp = str(time.time())
    http_uri = "/v1/audios"

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri+"?bucket_name="+bucket+"&page="+str(page)
    r = requests.get(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def update_audio(bucket, acr_id, title, audio_id, custom_fields=None):
    http_method = "PUT"
    timestamp = str(time.time())
    http_uri = "/v1/audios/"+acr_id

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    data = {'title':title, "audio_id":audio_id, "bucket_name":bucket}
    if custom_fields:
        keys = []
        values = []
        for k in custom_fields:
            keys.append(k)
            values.append(custom_fields[k])
        data['custom_key[]'] = keys
        data['custom_value[]'] = values

    requrl = "https://"+option['host'] + http_uri
    r = requests.put(requrl, data=data, headers=headers, verify=True)
    r.encoding = "utf-8"
    print r.text

def delete_audio(acr_id):
    http_method = "DELETE"
    timestamp = str(time.time())
    http_uri = "/v1/audios/"+acr_id

    string_to_sign = '\n'.join((http_method, http_uri, option['access_key'], option['signature_version'], str(timestamp)))
    signature = sign(string_to_sign, option['access_secret'])
    headers = {'access-key': option['access_key'], 'signature-version': option['signature_version'], 'signature': signature, 'timestamp':timestamp}

    requrl = "https://"+option['host'] + http_uri
    r = requests.delete(requrl, headers=headers, verify=True)
    r.encoding = "utf-8"
    if r.status_code == 204:
        print "deleted"

if __name__ == "__main__":
    #update_audio('eu-test', 'db397154fb9858f17373b5bf66be875a', 'Hiding my heart - Adele', '12345', {"artist":"Adele", "title":"Hiding my heart"})
    #delete_audio("07221fadacc359fdb0744cd28b7b0ce9")
    #get_audios('eu-test', 1)
    upload_audio(sys.argv[1], 'eu-test', 'test-title', '1212', 'fingerprint')

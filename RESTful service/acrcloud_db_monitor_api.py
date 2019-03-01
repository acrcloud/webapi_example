#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import time
import hmac
import json
import base64
import hashlib
import requests
import traceback

reload(sys)
sys.setdefaultencoding("utf8")

"""
This demo shows how to use the RESTful API to operate ACRCloud Broadcast Database Monitoring(project, channel, results)
You can find account_access_key and account_access_secret in your account page.
Log into http://console.acrcloud.com -> "Your Name"(top right corner) -> "Account" -> "Console API Keys" -> "Create Key Pair".
Be Careful, they are different with access_key and access_secret of your project.
"""


class Acrcloud_Monitor_API:

    def __init__(self, account_access_key, account_access_secret):
        self.account_access_key = account_access_key
        self.account_access_secret = account_access_secret

    def create_headers(self, http_uri, http_method, signature_version):
        timestamp = time.time()
        string_to_sign = "\n".join([http_method, http_uri, self.account_access_key, signature_version, str(timestamp)])
        sign = base64.b64encode(hmac.new(self.account_access_secret, string_to_sign, digestmod=hashlib.sha1).digest())
        headers = {
            "access-key": self.account_access_key,
            "signature-version": signature_version,
            "signature": sign,
            "timestamp": timestamp
        }
        return headers

    def get_project_channels(self, project_name, page_num=1):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams"
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"project_name":project_name, "page":page_num}
        r = requests.get(requrl, params=params, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def get_channel_info(self, channel_id):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/{0}".format(channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        r = requests.get(requrl, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def get_channel_results(self, project_name, channel_id, date):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/{0}/results".format(channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"project_name":project_name, "date":date}
        r = requests.get(requrl, params=params, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text


class Acrcloud_Monitor_Demo:

    def __init__(self, config):
        self.config = config
        self.api = Acrcloud_Monitor_API(self.config["account_access_key"], self.config["account_access_secret"])

    def all_project_channels(self, project_name):
        try:
            stream_list = []
            page_num = 1
            while 1:
                info = self.api.get_project_channels(project_name, page_num)
                jsoninfo = json.loads(info)
                for item in jsoninfo["items"]:
                    stream_list.append(item)
                #print jsoninfo["_meta"]
                if jsoninfo["_meta"]["currentPage"] == jsoninfo["_meta"]["pageCount"] :
                    break
                page_num += 1
            #print "Project:{0}, Total number of channels: {1}".format(project_name, len(stream_list))
        except Exception as e:
            traceback.print_exc()
        return stream_list

    def channel_info(self, channel_id):
        return self.api.get_channel_info(channel_id)

    def channel_results(self, project_name, channel_id, date):
        results = self.api.get_channel_results(project_name, channel_id, date)
        jresults = json.loads(results)
        return jresults

if __name__ == "__main__":
    config = {
        "account_access_key" : "XXXX",
        "account_access_secret" : "XXXXXX",
    }

    ams = Acrcloud_Monitor_Demo(config)

    project_name = "<your project name>"
    print ams.all_project_channels(project_name)

    channel_id = "<acrcloud db channel id>"
    print ams.channel_info(channel_id)

    project_name = "<your project name>"
    channel_id = "<acrcloud db channel id>"
    date = "20190228"
    rlist = ams.channel_results(project_name, channel_id, date)
    for item in rlist:
        print item

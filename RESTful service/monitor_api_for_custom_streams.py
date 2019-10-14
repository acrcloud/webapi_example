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
This demo shows how to use the RESTful API to operate Broadcast Monitoring(Custom Streams)
You can find account_access_key and account_access_secret in your account page.
Log into http://console.acrcloud.com -> "Your Name"(top right corner) -> "Account" -> "Console API Keys" -> "Create Key Pair".
Be Careful, they are different with access_key and access_secret of your project.
"""


class Acrcloud_Monitor_API_for_custom_streams:

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
            "timestamp": str(timestamp)
        }
        return headers

    def get_project_channels(self, project_name, page_num=1):
        requrl = "https://api.acrcloud.com/v1/monitor-streams"
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"project_name":project_name, "page":page_num}
        r = requests.get(requrl, params=params, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def add_channel(self, project_name, stream_name, region, url):
        requrl = "https://api.acrcloud.com/v1/monitor-streams"
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "POST"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        data = {
            "project_name" : project_name,
            "stream_name": stream_name,
            "region": region,
            "url": url,
            "realtime": 0
        }
        r = requests.post(requrl, data=data, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def delete_channel(self, stream_id):
        requrl = "https://api.acrcloud.com/v1/monitor-streams/{0}".format(stream_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "DELETE"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        r = requests.delete(requrl, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def pause_restart_channel(self, stream_id, action_type="pause"):
        #action_type:  1. pause, 2. restart
        requrl = "https://api.acrcloud.com/v1/monitor-streams/{0}/{1}".format(stream_id, action_type)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "PUT"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        r = requests.put(requrl, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def update_channel(self, stream_id, update_info):
        requrl = "https://api.acrcloud.com/v1/monitor-streams/{0}".format(stream_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "PUT"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        """
        update_info = {
            "stream_name":"xxx",
            "url":"xxxx",
            "region":"xxxx",
            "realtime":0,  #0-realtime, 1-delay
        }
        """
        r = requests.put(requrl, data=update_info, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def set_callback(self, project_access_key, callback_url, post_type="json"):
        requrl = "https://ap-api.acrcloud.com/v1/monitors/{0}/callback".format(project_access_key)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "POST"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        data = {
            "callback_url":callback_url,
            "post_type":post_type, #json or form
        }

        r = requests.post(requrl, data=data, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text


class Custom_Monitor_Demo:

    def __init__(self, config):
        self.config = config
        self.project_name = self.config["project_name"]
        self.project_access_key = self.config["project_access_key"]
        self.api = Acrcloud_Monitor_API_for_custom_streams(self.config["account_access_key"], self.config["account_access_secret"])

    def all_project_channels(self):
        try:
            stream_list = []
            page_num = 1
            while 1:
                info = self.api.get_project_channels(self.project_name, page_num)
                jsoninfo = json.loads(info)
                for item in jsoninfo["items"]:
                    stream_list.append(item)
                #print jsoninfo["_meta"]
                if jsoninfo["_meta"]["currentPage"] == jsoninfo["_meta"]["pageCount"] :
                    break
                page_num += 1
            print "Project:{0}, Total number of channels: {1}".format(self.project_name, len(stream_list))
        except Exception as e:
            traceback.print_exc()
        return stream_list

    def add_monitor(self, stream_name, region, url):
        print "Add stream: {0}, {1}, {2}".format(stream_name, region, self.api.add_channel(self.project_name, stream_name, region, url))

    def del_monitor(self, stream_id):
        print "Delete stream: {0}, {1}".format(stream_id, self.api.delete_channel(stream_id))

    def pause_restart_monitor(self, stream_id, action_type="pause"):
        print "{0} stream: {1}, {2}".format(action_type, stream_id, self.api.pause_restart_channel(stream_id, action_type))

    def update_monitor(self, stream_id, update_info):
        if update_info:
            print "update stream: {0}, {1}".format(stream_id, self.api.update_channel(stream_id, update_info))
        else:
            print "update info is None, ", stream_id

    def set_callback(self, callback_url, post_type):
        print "set callback: ", callback_url, self.api.set_callback(self.project_access_key, callback_url, post_type)


if __name__ == "__main__":
    config = {
        "account_access_key" : "<<< your account access_key >>>",
        "account_access_secret" : "<<< your account access_secret >>>",
        "project_name":"<<<your project name >>>",
        "project_access_key":"<<< your project access_key >>>",
    }

    ams = Custom_Monitor_Demo(config)
    print ams.all_project_channels()
    #print ams.add_monitor("api_add", "ap-northeast-1", "http://xxxx")

    #stream_id="XXXX"
    #ams.pause_restart_monitor(stream_id, "restart") #pause  or restart
    #ams.update_monitor(stream_id, {"stream_name":"xxxx"})

    #callback_url = "www.xxxx.com"
    #ams.set_callback(callback_url, "form")

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

    def get_projects(self):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/projects"
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        r = requests.get(requrl, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def set_result_callback(self, project_name, result_callback_url, send_noresult=False, post_data_type="json", result_type="realtime"):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/projects/result_callback"
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "POST"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        data = {
            "project_name":project_name,
            "url":result_callback_url,
            "send_noresult":send_noresult,
            "post_data_type":post_data_type,
            "result_type":result_type,
        }
        r = requests.post(requrl, data=data, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def set_state_callback(self, project_name, state_callback_url, post_data_type="json"):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/projects/state_callback"
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "POST"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        data = {
            "project_name":project_name,
            "url":state_callback_url,
            "post_data_type":post_data_type,
        }
        r = requests.post(requrl, data=data, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

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

    def get_channel_urls(self, channel_id):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/{0}/urls".format(channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        r = requests.get(requrl, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def del_channel_urls(self, channel_id, del_url_list):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/{0}/urls".format(channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "DELETE"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        data = {"del_urls":json.dumps(del_url_list)}
        r = requests.delete(requrl, data=data, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def add_channel_urls(self, channel_id, add_url_list):
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/{0}/urls".format(channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "POST"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"add_urls":json.dumps(add_url_list)}
        r = requests.post(requrl, data=data, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def download_rec_recording(self, access_key, channel_id, record_timestamp, played_duration):
        "GET,HEAD <module>/acrcloud-monitor-streams/recording/"
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/recording/{0}/{1}".format(access_key, channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"record_timestamp":record_timestamp, "played_duration":played_duration}
        r = requests.get(requrl, params=params, headers=headers, verify=True)
        try:
            d = r.headers['content-disposition']
            fname = d[ (d.find('filename="') + len('filename="')) : d.find('";') ]
            fname = fname.replace(":", "_")
        except Exception as e:
            fname = "acrcloud_{0}_{1}_{2}.failed".format(channel_id, record_timestamp, played_duration)
        return fname, r.content

    def get_day_recording_list(self, project_access_key, channel_id, date):
        "GET,HEAD <module>/acrcloud-monitor-streams/recording_list/"
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/recording_list/{0}/{1}".format(project_access_key, channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"date":date}
        r = requests.get(requrl, params=params, headers=headers, verify=True)
        r.encoding = "utf-8"
        return r.text

    def download_hour_recording(self, project_access_key, channel_id, timestamp, duration, file_type):
        "GET,HEAD <module>/acrcloud-monitor-streams/recording_download/"
        requrl = "https://api.acrcloud.com/v1/acrcloud-monitor-streams/recording_download/{0}/{1}".format(project_access_key, channel_id)
        http_uri = requrl[requrl.find("/v1/"):]
        http_method = "GET"
        signature_version = "1"

        headers = self.create_headers(http_uri, http_method, signature_version)
        params = {"timestamp":timestamp, "duration": duration, "type": file_type}
        r = requests.get(requrl, params=params, headers=headers, verify=True)
        try:
            d = r.headers['content-disposition']
            fname = d[ (d.find('filename="') + len('filename="')) : d.find('";') ]
            fname = fname.replace(":", "_")
        except Exception as e:
            timestamp_f = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            fname = "acrcloud_{0}_{1}_{2}.failed".format(channel_id, timestamp_f, duration)
        return fname, r.content

class Acrcloud_Monitor_Demo:

    def __init__(self, config):
        self.config = config
        self.api = Acrcloud_Monitor_API(self.config["account_access_key"], self.config["account_access_secret"])

    def projects(self):
        try:
            info = self.api.get_projects()
            jinfo = json.loads(info)
            return jinfo["data"]
        except Exception as e:
            traceback.print_exc()
        return []

    def set_state_callback(self, project_name, state_callback_url, post_data_type="json"):
        """
        post_data_type: "json" or "form"
        """
        try:
            if state_callback_url:
                return self.api.set_state_callback(project_name, state_callback_url, post_data_type)
        except Exception as e:
            traceback.print_exc()
        return None

    def set_result_callback(self, project_name, result_callback_url, send_noresult=False, post_data_type="json", result_type="realtime"):
        """
        send_noresult: True or False
        post_data_type: "json" or "form"
        result_type: "realtime" or "delay"
        """
        try:
            if result_callback_url:
                return self.api.set_result_callback(project_name, result_callback_url, send_noresult, post_data_type, result_type)
        except Exception as e:
            traceback.print_exc()
        return None

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

    def get_channel_urls(self, channel_id):
        urls = self.api.get_channel_urls(channel_id)
        jurls = json.loads(urls)
        return jurls

    def add_channel_urls(self, channel_id, add_urls):
        ret = self.api.add_channel_urls(channel_id, add_urls)
        return ret

    def del_channel_urls(self, channel_id, del_urls):
        ret = self.api.del_channel_urls(channel_id, del_urls)
        return ret

    def download_rec_recording(self, access_key, channel_id, record_timestamp, played_duration):
        fname, content = self.api.download_rec_recording(access_key, channel_id, record_timestamp, played_duration)
        return fname, content

    def get_day_recording_list(self, access_key, channel_id, date):
        ret = self.api.get_day_recording_list(access_key, channel_id, date)
        recording_list = json.loads(ret)
        return recording_list

    def download_hour_recording(self, access_key, channel_id, timestamp, duration, file_type):
        fname, content = self.api.download_hour_recording(access_key, channel_id, timestamp, duration, file_type)
        return fname, content

if __name__ == "__main__":
    config = {
        "account_access_key" : "XXXX",
        "account_access_secret" : "XXXXXXXXXX",
    }

    ams = Acrcloud_Monitor_Demo(config)

    """
    #Get all the projects
    project_list = ams.projects()
    """

    """
    #Set State Callback_URL
    #post_data_type: "json" or "form"
    ams.set_state_callback("<project_name>", "<state_callback_url>", "json")
    """

    """
    #Set Result Callback_URL
    #send_noresult: True or False
    #post_data_type: "json" or "form"
    #result_type: "realtime" or "delay"
    print ams.set_result_callback("<project_name>", "<result_callback_url>", False, "form", "realtime")
    """

    """
    project_name = "<your project name>"
    print ams.all_project_channels(project_name)

    channel_id = "<acrcloud db channel id>"
    print ams.channel_info(channel_id)
    """

    """
    channel_id = "XXXXX"
    print ams.get_channel_urls(channel_id)
    add_url_list = ["url1"]
    print ams.add_channel_urls(channel_id, add_url_list)
    print ams.get_channel_urls(channel_id)
    del_url_list = ["url1"]
    print ams.del_channel_urls(channel_id, del_url_list)
    """

    """
    # download rec recording
    access_key = "<your project access_key>"
    channel_id = "<channel_id>"
    record_timestamp = "20191203131312"
    played_duration = 100
    fname, fcontent = ams.download_rec_recording(access_key, channel_id, record_timestamp, played_duration)
    if not fname.endswith("failed"):
        with open(fname, "wb") as wfile:
            wfile.write(fcontent)
    """

    """
    # download hour recording
    access_key = "<your project access_key>"
    channel_id = "<channel_id>"
    date = "<YYYYMMDD>"
    jinfo = ams.get_day_recording_list(access_key, channel_id, date)
    for item in jinfo["data"]:
        print item
        timestamp = item["timestamp"]
        duration = item["duration"]
        file_type = item["type"]
        fname, fcontent = ams.download_hour_recording(access_key, channel_id, timestamp, duration, file_type)
        print fname
        with open(fname, "wb") as wfile:
            wfile.write(fcontent)
    """

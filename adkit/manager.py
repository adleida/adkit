#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: adkit/manager.py
# Author: fanyongtao
# mail: jacketfan826@gmail.com
# Created Time: 2015年05月10日 星期日 11时16分05秒
#########################################################################
import logging
from . cli import Client
from . utils import compare_dictionaries


class TestManager(object):

    def __init__(self, conf=None, ex_url=None, mock_url=None, log_url=None):
        self.cli = Client()
        self.conf = conf or {}
        self.ex_url = ex_url or 'http://127.0.0.1:5000/reload'
        self.mock_url = mock_url or 'http://127.0.0.1:6001/conf'
        self.log_url = log_url or 'http://127.0.0.1:6001/log/'

    def set_url(self, url=None):
        self.cli.url = url


    def reload_conf(self):
        self.set_url(url=self.ex_url)
        self.cli.post_json_data()
        return self.cli.res.json()

    def send_conf(self):
        self.set_url(url=self.mock_url)
        self.cli.post_json_data(json=self.conf)
        return self.cli.res.json()

    def setup(self):
        cf = self.send_conf()
        rc = self.reload_conf()
        # print(cf, rc)
        if cf.get('conf', False) and rc.get('reload', False):
            return cf.get('uuid', ''), True 
        else:
            return None, False

    def send_bid(self,url, data):
        self.set_url(url=url)
        try:
            self.cli.post_json_data(json=data)
            return self.cli.res.json()
        except Exception as ex:
            self.cli.post_normal_data(data=data)
            return self.cli.res.json()

    def final_result(self, url, data, result):
        bid_result = self.send_bid(url, data)
        print("case response = %s" % (bid_result))
        try:
            compare_dictionaries(bid_result, result)
            return True
        except Exception as ex:
            return False

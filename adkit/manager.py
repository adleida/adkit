#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: adkit/manager.py
# Author: fanyongtao
# mail: jacketfan826@gmail.com
# Created Time: 2015年05月10日 星期日 11时16分05秒
#########################################################################
import logging
import os.path as _path
from . cli import Client
from . utils import compare_dictionaries, load_conf, update_request


class TestManager(object):

    def __init__(self, ex=None, mock=None):
        self.cli = Client()
        self.conf = conf or {}
        self.ex = ex or 'http://127.0.0.1:5000'
        self.mock = mock or 'http://127.0.0.1:6001'
        self.rt = {}
        self.make_url()

    def set_url(self, url=None):
        self.cli.url = url

    def make_url(self):
        self.ex_reload = _path.join(self.ex, 'reload')
        self.ex_bid = _path.join(self.ex, 'clk')
        self.mock_conf = _path.join(self.mock, 'conf')

    def reload_conf(self):
        self.set_url(url=self.ex_reload)
        self.cli.post_json_data()
        return self.cli.res.json()

    def send_conf(self, obj):
        self.set_url(url=self.mock_conf)
        self.cli.post_json_data(json=obj)
        return self.cli.res.json()

    def setup(self):
        cf = self.send_conf()
        rc = self.reload_conf()
        if cf.get('conf', False) and rc.get('reload', False):
            return cf.get('uuid', ''), True 
        return None, False

    def send_bid(self, data):
        self.set_url(url=sefl.ex_bid)
        try:
            self.cli.post_json_data(json=data)
            return self.cli.res.json()
        except Exception as ex:
            self.cli.post_normal_data(data=data)
            return self.cli.res.json()

    def final_result(self, data, result):
        bid_result = self.send_bid(data)
        print("case response = %s" % (bid_result))
        try:
            compare_dictionaries(bid_result, result)
            return True
        except Exception as ex:
            return False

    def re_test(self, folder=None, count=1):
        target_file = 'config.yaml'
        os.chdir(folder)
        for obj in os.listdir(os.curdir):
            if obj == target_file:
                su = self.setup()
                if su[1]:
                    self.rt['uid'] = su[0]
            if os.path.isdir(obj) :
                scandir(obj, target)
                os.chdir(os.pardir) #!!!


#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: adkit/cliagent.py
# Author: fanyongtao
# mail: jacketfan826@gmail.com
# Created Time: 2015年05月13日 星期三 00时26分59秒
#########################################################################
import os
import os.path as _path
import requests
import logging
from .utils import load_conf, compare_dictionaries

logger = logging.getLogger(__name__)


class CliAgent(object):

    def __init__(self, ex=None, mock=None):
        self.ex = ex or 'http://127.0.0.1:5000'
        self.mock = mock or 'http://127.0.0.1:6001'
        self.header = {"Content-Type": "application/json"}
        self.case = []
        self.make_url()

    def make_header(self, **kwargs):
        self.header.update(kwargs)

    def make_url(self):
        self.ex_reload = _path.join(self.ex, 'reload')
        self.ex_bid = _path.join(self.ex, 'clk')
        self.mock_conf = _path.join(self.mock, 'conf')

    def send_conf(self, json):
        return requests.post(self.mock_conf, json=json)

    def reload_conf(self):
        return requests.post(self.ex_reload, json={})

    def setup(self, json):
        sc = self.send_conf(json=json).json()
        rc = self.reload_conf().json()
        if sc['conf'] and rc['reload']:
            logging.info('setup,success!!!')
            return sc['uuid']
        logging.info('setup,fail!!!')
        return None

    def send_bid(self, fname='request.json', timeout=1):
        req_data = load_conf(fname)
        return requests.post(self.ex_bid, json=req_data, timeout=timeout,
                             headers=self.header)

    def final_result(self, result='result.json', timeout=1):
        bid_result = self.send_bid(timeout=timeout)
        logging.debug('bid_result: %s' % bid_result.json())
        result = load_conf(result)
        try:
            compare_dictionaries(bid_result.json(), result)
            logging.info('final_result: True')
            return True
        except Exception as ex:
            logging.info('final_result: False')
            logging.error('final_result: %s' % ex)
            return False
    
    def gen_case_dir(self, folder):
        target = 'config.yaml'
        os.chdir(folder)
        for obj in os.listdir(os.curdir) :
            if obj == target :
                self.case.append(os.getcwd())
            if os.path.isdir(obj) :
                self.gen_case_dir(obj)
                os.chdir(os.pardir) #!!!

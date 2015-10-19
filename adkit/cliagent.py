#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: adkit/cliagent.py
# Author: fanyongtao
# mail: jacketfan826@gmail.com
# Created Time: 2015年05月13日 星期三 00时26分59秒
#########################################################################
from dictdiffer import diff
import os
import time
import os.path as _path
import requests
import logging
import codecs
from .utils import load_conf, compare_dictionaries, update_request
from .exception import SetupException, ReloadException, ConfException,\
    SendbidExcecption

logger = logging.getLogger(__name__)


class CliAgent(object):

    def __init__(self, ex=None, mock=None, headers=None):
        self.ex = ex or 'http://127.0.0.1:5000'
        self.mock = mock or 'http://127.0.0.1:6001'
        self.header = headers or {"Content-Type": "application/json"}
        self.case = []
        self.ignore = []
        self.make_url()

    def make_header(self, **kwargs):
        self.header.update(kwargs)

    def make_url(self):
        self.ex_reload = _path.join(self.ex, 'reload')
        self.ex_bid = _path.join(self.ex, 'clk')
        self.mock_conf = _path.join(self.mock, 'conf')

    def send_conf(self, json):
        try:
            tt = requests.post(self.mock_conf, json=json)
            logging.info("send_conf: (pass, None)")
            return tt
        except Exception as ex:
            logging.error("send_conf: (fail, %s)" % ex)
            raise ConfException("send_conf error, reason: %s" % ex)

    def reload_conf(self, json=None):
        if json is None:
            json = {}
        try:
            tt = requests.post(self.ex_reload, json=json)
            logging.info("reload_conf: (pass, None)")
            return tt
        except Exception as ex:
            logging.error("reload_conf: (fail, %s)" % ex)
            raise ReloadException("Reload error, reason: %s" % ex)

    def setup(self, json):
        try:
            dsps = {
                "dsps": json["dsp"]["s"]
            }
            sc = self.send_conf(json=json).json()
            rc = self.reload_conf(json=dsps)
            if sc['conf']:
                logging.info("setup: (pass, None)")
                return sc['uuid']
        except Exception as ex:
            logging.error("setup:(fail, %s)" % ex)
            raise SetupException("Setup Error, reason: %s" % ex)

    def send_bid(self, fname='request.json', timeout=1):
        try:
            with codecs.open(fname, encoding='utf8') as f:
                req_data = f.read().encode()
                console.log(req_data);
                tt = requests.post(self.ex_bid, data=req_data, timeout=timeout, headers=self.header)
                logging.info("send_bid: (pass, %s)" % tt.json())
                return tt
        except ValueError as vex:
            logging.error("send_bid: (pass, But response format error: %s)" % vex)
        except Exception as ex:
            logging.error("send_bid: (fail, %s)" % ex)
            raise SendbidExcecption("Send_bid error, reason: %s" % ex)

    def final_result(self, result='result.json', timeout=1):
        try:
            bid_result = self.send_bid(timeout=timeout)
            result = load_conf(result)
            re = diff(bid_result.json(), result)
            re = list(re)
            if re:
                for item in re:
                    if "change" in item:
                        raise Exception(str(item))
        except SendbidExcecption as ex:
            raise SendbidExcecption("Send_bid error, reason: %s" % ex)
        except Exception as eex:
            raise eex

    def gen_case_dir(self, folder):
        ignore = 'ignore'
        target = 'config.yaml'
        os.chdir(folder)
        if ignore in os.listdir(os.curdir):
            self.ignore.append(os.getcwd())
        elif target in os.listdir(os.curdir):
            self.case.append(os.getcwd())
        for obj in os.listdir(os.curdir):
            if os.path.isdir(obj):
                self.gen_case_dir(obj)
                os.chdir(os.pardir)

    def run_normal(self, timeout=1):
        for ce in self.case:
            start = time.time()
            try:
                result = self.send_bid(timeout=timeout).json()
                logging.info("bid_response: (pass, %s)" % result)
            except SendbidExcecption as ex:
                logging.error("bid_response: (fail, %s)" % ex)
            except Exception as aex:
                logging.error("bid_response: (fail, %s)" % aex)
            end = time.time()
            logging.info('case_name = %s, escape_time = %s' % (ce, (end - start)))

    def run_forever(self, timeout=1):
        while True:
            for ce in self.case:
                start = time.time()
                logging.info('case_name = %s' % ce)
                try:
                    os.chdir(ce)
                    self.setup(update_request(load_conf('config.yaml')))
                    self.final_result(timeout=timeout)
                    logging.info("final_result: (pass, None)")
                except SetupException as setex:
                    logging.error("send_bid: (fail, %s)" % setex)
                    logging.error("final_result: (fail, %s)" % setex)
                except SendbidExcecption as sendex:
                    logging.error("final_result: (fail, %s)" % sendex)
                except Exception as cex:
                    logging.error("final_result: (fail, %s)" % cex)
                end = time.time()
                logging.info("case_escaped_time:%s" % (end - start))
                continue

    def run_case(self, count=1, timeout=1):
        for ce in self.case:
            logging.info('case_name = %s' % ce)
            os.chdir(ce)
            self.setup(update_request(load_conf('config.yaml')))
            start = time.time()
            for ct in range(count):
                try:
                    logging.info("Count: %s" % (ct + 1))
                    self.final_result(timeout=timeout)
                except Exception as ex:
                    logging.error('final_result: (fail, %s)' % ex)
                else:
                    logging.info('final_result: (pass, None)')
                continue
            end = time.time()
            yield (ce, count, (end - start) / count)

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: adkit/case.py
# Author: fanyongtao
# mail: jacketfan826@gmail.com
# Created Time: 2015年05月10日 星期日 15时52分47秒
#########################################################################

from . manager import TestManager
import argparse
import os
import time
import os.path
from . utils import load_conf, update_request, load_file, compare_dictionaries
import json
import logging
from . utils import load_file
jj = list() 


def init():
    cfg = load_conf('config.yaml')
    cfg = update_request(cfg)
    tm = TestManager(cfg)
    return tm, cfg


def one(fuck=None):
    if fuck is None:
        fuck = {}
    tm, cfg = init()
    re, ok = tm.setup()
    if ok:
        req_tmp = load_file('request.json')
        result_tmp = load_file('result.json')
        bid_url = 'http://{}/clk'.format(cfg.get('bind', '127.0.0.1:5000'))
        log_url = tm.log_url + str(re)
        fuck['case'] = os.getcwd()
        fuck['final_result'] = tm.final_result(bid_url, req_tmp, result_tmp)
        fuck['log_url'] = log_url
    else:
        logging.error('setup error')
        exit(-1)
    return fuck

def scandir(startdir, target='config.yaml'):
    os.chdir(startdir)
    for obj in os.listdir(os.curdir) :
        if obj == target :
            try:
                kit = one()
                jj.append(kit)
            except Exception as ex:
                print(ex)
        if os.path.isdir(obj) :
            scandir(obj, target)
            os.chdir(os.pardir) #!!!


def get_arg():
    parser = argparse.ArgumentParser(description='ad-client')
    parser.add_argument('-f', '--folder',dest='folder', type=str,
                        required=True,
                        help='The case folder')
    parser.add_argument('-n', '--count',dest='count', type=int,
                        default=100,
                        help='an integer for the accumulator')
    args = parser.parse_args()
    return args
    pass

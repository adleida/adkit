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
import adkit



def get_arg():
    parser = argparse.ArgumentParser(description='adlei test kit')
    parser.add_argument('-f', '--folder',dest='folder', type=str, required=True, help='The case folder')
    parser.add_argument('-n', '--count',dest='count', type=int, default=1, help='count')
    parser.add_argument('-r', '--forover',dest='forover', type=bool, default=False, help='for_over test')
    parser.add_argument('-v', action='version',version=adkit.__version__)
    args = parser.parse_args()
    return args


def test_case(case, tm, count=1):
    os.chdir(case)
    for cut in range(count):
        result = {}
        # load_test data
        try:
            cfg = load_conf('config.yaml')
            cfg = update_request(cfg)
            request_tmp = load_file('request.json')
            result_tmp = load_file('result.json')
            su = tm.setup(cfg)
            if su[1]:
                final = tm.final_result(request_tmp, result_tmp)
                result['final_result'] = final
                result['case'] = case
                result['uuid'] = su[0]
                yield result
        except Exception as ex:
            print(case, ex)
            break

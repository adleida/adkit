#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: adkit/case.py
# Author: fanyongtao
# mail: jacketfan826@gmail.com
# Created Time: 2015年05月10日 星期日 15时52分47秒
#########################################################################

import argparse
import adkit


def get_arg():
    """get the args"""

    parser = argparse.ArgumentParser(description='adlei test kit')
    parser.add_argument('-f', '--folder', dest='folder', type=str, required=True,
                        help='The case folder')

    parser.add_argument('-n', '--count', dest='count', type=int, default=1,
                        help='count')

    parser.add_argument('-r', '--forover', dest='forover', type=bool, default=False,
                        help='for_over test')

    parser.add_argument('-v', action='version', version=adkit.__version__)
    args = parser.parse_args()
    return args

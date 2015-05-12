#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import argparse
from . report import gen_report
from . case import get_arg, test_case
from . utils import load_resource, load_conf, update_request, load_file
from . manager import TestManager
import webbrowser


def main():
    args = get_arg()
    cloud = load_resource('adkit.yaml')
    ex = cloud.get('ex')
    mock = cloud.get('mock')

    tm = TestManager(ex=ex, mock=mock)
    tm.gen_case_dir(args.folder)
    
    def for_over():
        while True:
            for x in tm.case:
                for y in test_case(x, tm, args.count):
                    print(y)
    def test_n():
        for x in tm.case:
            for y in test_case(x, tm, args.count):
                yield(y)

    if args.forover:
        for_over()
    else:
        for re in test_n():
            print(re)
        


if __name__ == '__main__':

    main()

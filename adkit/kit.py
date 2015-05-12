#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import argparse
from . report import gen_report
from . case import get_arg
from . utils import load_resource, load_conf, update_request, load_file
from . manager import TestManager
import webbrowser


def main():
    # args = get_arg()
    # # a = load_resource('adkit.json')
    # if os.path.exists(args.folder):
    #     if args.count:
    #         scandir(args.folder, count=args.count)
    #     else:
    #         scandir(args.folder)

    #     data = load_resource('report.html', as_object=False)
    #     gen_report(data)
    # else:
    #     print("folder not found")
    #     exit(-2)
    cfg = load_conf('config.yaml')
    cfg = update_request(cfg)
    request_tmp = load_file('request.json')
    result_tmp = load_file('result.json')
    tm = TestManager()
    final = tm.final_result(request_tmp, result_tmp)
    print(final)
    print(tm.mock_conf, tm.ex_bid, tm.ex_reload)


if __name__ == '__main__':

    main()

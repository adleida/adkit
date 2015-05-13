#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import argparse
# from . report import gen_report
from . utils import load_resource, load_conf, update_request, load_file
# from . manager import TestManager
from .cliagent import CliAgent
import time
import logging
import logging.config
import adkit

logger = logging.getLogger(__name__)

def get_arg():
    parser = argparse.ArgumentParser(description='adlei test kit')
    parser.add_argument('-f', '--folder',dest='folder', type=str, required=True, help='The case folder')
    parser.add_argument('-n', '--count',dest='count', type=int, default=1, help='count')
    parser.add_argument('-t', '--timeout',dest='timeout', type=float, default=1, help='timeout')
    parser.add_argument('-v', action='version',version=adkit.__version__)
    args = parser.parse_args()
    return args

def main():
    
    args = get_arg()
    cloud = load_resource('adkit.yaml')
    ca = CliAgent(ex=cloud.get('ex'), mock=cloud.get('mock'))
    ca.gen_case_dir(args.folder)

    log = cloud.get('logging', {})
    log.setdefault('version', 1)
    logging.config.dictConfig(log)

    for x in range(args.count or 5000000):
        start = time.time()
        logging.info('count: %d' %(x+1))
        for ff in ca.case:
            logging.info('case: %s' % ff)
            os.chdir(ff)
            try:
                conf = update_request(load_conf('config.yaml'))
                uid = ca.setup(conf)
                logging.info('uuid: %s' % uid)
            except Exception as ex:
                logging.error('case: %s' % ff)
                logging.error('error: %s' % ex)
                continue
            else:
                try:
                    ca.final_result(timeout=args.timeout)
                except Exception as ex:
                    logging.error('recv_response: False')
                    logging.error('send_bid_error: %s' % ex)
                    continue
        end = time.time()
        logging.info('use time %s' %(end - start))
    # 
    # def for_over():
    #     while True:
    #         for x in tm.case:
    #             for y in test_case(x, tm, args.count):
    #                 print(y)
    # def test_n():
    #     for x in tm.case:
    #         for y in test_case(x, tm, args.count):
    #             yield(y)

    # if args.forover:
    #     for_over()
    # else:
    #     for re in test_n():
    #         print(re)
        


if __name__ == '__main__':

    main()

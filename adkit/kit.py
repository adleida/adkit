#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import argparse
from . utils import load_resource, load_conf, update_request
from .cliagent import CliAgent
import time
import logging
import logging.config
import adkit

logger = logging.getLogger(__name__)


def get_arg():
    parser = argparse.ArgumentParser(description='adlei test kit')
    parser.add_argument('-f', '--folder', dest='folder', type=str, default='.',
                        required=False, help='The case folder')
    parser.add_argument('-n', '--count', dest='count', type=int, default=1, help='count')
    parser.add_argument('-t', '--timeout', dest='timeout', type=float, default=1, help='timeout')
    parser.add_argument('-v', action='version', version=adkit.__version__)
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

    try:
        ss = time.time()
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
                for x in range(args.count or 5000000):
                    start = time.time()
                    try:
                        logging.info('count: %d' % (x+1))
                        ca.final_result(timeout=args.timeout)
                        end = time.time()
                        use_time = end - start
                        logging.info('use_time: %s' % (use_time))
                    except Exception as ex:
                        logging.error('recv_response: False')
                        logging.error('send_bid_error: %s' % ex)
                    continue
    except KeyboardInterrupt as ex:
        ee =time.time()
        logging.info("running_time = %.3f 's"%(ee - ss))


if __name__ == '__main__':

    main()

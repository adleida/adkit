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
from tabulate import tabulate

logger = logging.getLogger(__name__)


def get_arg():
    parser = argparse.ArgumentParser(description='adlei test kit')

    parser.add_argument('-f', '--folder', dest='folder', type=str,
                        default='.', required=False, help='The case folder')

    parser.add_argument('-n', '--count', dest='count', type=int, default=1,
                        help='count')

    parser.add_argument('-t', '--timeout', dest='timeout', type=float,
                        default=1, help='timeout')

    parser.add_argument('-c', '--config', dest='config', required=True, type=str, help='config file')

    parser.add_argument('--forever', action='store_true',
                        help='run the case forover')

    parser.add_argument('--normal', action='store_true',
                        help='send bid normal')
    parser.add_argument('-v', action='version', version=adkit.__version__)
    args = parser.parse_args()
    return args


def main():
    args = get_arg()
    cloud = load_conf(args.config)
    ca = CliAgent(ex=cloud.get('ex'), mock=cloud.get('mock'), headers=cloud.get('req_header', {}))
    ca.gen_case_dir(args.folder)

    log = cloud.get('logging', {})
    log.setdefault('version', 1)
    logging.config.dictConfig(log)

    if args.normal:
        if args.forever:
            try:
                start7 = time.time()
                while True:
                    try:
                        start = time.time()
                        ca.run_normal(args.timeout)
                        end1 = time.time()
                        logging.info("time %s" % (end1 - start))
                    except Exception as ex:
                        end2 = time.time()
                        logging.error("Error %s" % ex)
                        logging.info("time %s" % (end2 - start))
                        continue
            except KeyboardInterrupt:
                end7 = time.time()
                logging.warn("Run normal %s 's" % (end7 - start7))
                return
        if args.count:
            start5 = time.time()
            for x in range(args.count):
                ca.run_normal(timeout=args.timeout)
            end5 = time.time()
            logging.info("Normal avg time: %s" % ((end5 - start5) / args.count))
        return

    if args.forever:
        try:
            start = time.time()
            ca.run_forever(args.timeout)
        except KeyboardInterrupt:
            end2 = time.time()
            logging.warn('<<<<<<<<Test stop>>>>>>>>')
            logging.info("Take time: %s 's" % (end2 - start))
        return

    start = time.time()
    result = [x for x in ca.run_case(args.count, args.timeout)]
    end = time.time()
    logging.info("escaped_time %s's " % (end - start))
    for x, y, z in result:
        logging.info("{},{},{}".format(x, y, z))
    print(tabulate(result, headers=['case', 'count', 'avg_time']))
    print(tabulate([ca.ignore], headers=['ignore case']))


if __name__ == '__main__':
    main()

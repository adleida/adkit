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
    parser.add_argument('-f', '--folder', dest='folder', type=str, default='.', required=False, help='The case folder')
    parser.add_argument('-n', '--count', dest='count', type=int, default=1, help='count')
    parser.add_argument('-t', '--timeout', dest='timeout', type=float, default=1, help='timeout')
    parser.add_argument('--forover', action='store_true', help='run the case forover')
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

    if args.forover:
        try:
            start = time.time()
            ca.run_forover(args.timeout)
        except KeyboardInterrupt as ex:
            end = time.time()
            logging.warn('<<<<<<<<Test stop>>>>>>>>')
            logging.info("Take time: %s 's" % (end - start))
        return

    ca.run_case(args.count, args.timeout)


if __name__ == '__main__':

    main()

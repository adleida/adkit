#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import argparse
from . report import gen_report
from . case import get_arg, test_case
from . utils import load_resource, load_conf, update_request, load_file
from . manager import TestManager
from .cliagent import CliAgent
import webbrowser
import logging
import logging.config

logger = logging.getLogger(__name__)


def main():
    
    args = get_arg()
    cloud = load_resource('adkit.yaml')
    ca = CliAgent(ex=cloud.get('ex'), mock=cloud.get('mock'))
    ca.gen_case_dir(args.folder)

    log = cloud.get('logging', {})
    log.setdefault('version', 1)
    logging.config.dictConfig(log)

    for x in range(args.count):
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
                ca.final_result()
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

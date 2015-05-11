#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import argparse
from . report import gen_report
from . case import init, scandir, get_arg
from . utils import load_resource


def main():
    args = get_arg()
    if os.path.exists(args.folder):
        # scandir('/home/fan/project/tkit/docs/protocol-0.14/')
        scandir(args.folder)
        data = load_resource('report.html', as_object=False)
        gen_report(data)


if __name__ == '__main__':

    main()

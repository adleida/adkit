#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from jinja2 import Template
from . report import gen_report
from . case import init, scandir, jj
from . utils import load_resource


def main():

    scandir('/home/fan/project/tkit/docs/protocol-0.14/')
    data = load_resource('report.html', as_object=False)
    gen_report(data)

    print('jj = %s' % jj)


if __name__ == '__main__':

    main()

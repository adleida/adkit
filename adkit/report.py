#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import jinja2


def gen_report(data):
    template = jinja2.Template(data)
    with open('report.html', 'w') as tt:
        tt.write(template.render(jj=jj))

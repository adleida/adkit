#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    adkit.utils
    ~~~~~~~~~~~
    This module implements the utils
'''

import functools
import io
import json
import jsonschema
import os.path
import pkgutil
import requests
import yaml
import logging
import time


@functools.lru_cache()
def load_schema(name):

    name = '{}-schema.json'.format(name)
    obj = load_resource(name)
    schema = jsonschema.Draft4Validator(obj)
    return schema


@functools.lru_cache()
def load_resource(name, as_object=True):

    path = 'res/{}'.format(name)
    blob = pkgutil.get_data(__package__, path)
    if blob is None:
        raise Exception('no such resource: {}'.format(name))
    data = blob.decode()
    if as_object:
        ext = os.path.splitext(name)[-1]
        if ext in ['.json']:
            data = json.loads(data)
        elif ext in ['.yaml', '.yml']:
            data = yaml.load(io.StringIO(data))
        else:
            raise Exception('cannot detect resource type')
    return data


def check_schema(obj, schema):

    try:
        schema = load_schema(schema)
        schema.validate(obj)
        return True, None
    except Exception as ex:
        return False, Exception(ex.message)


def load_json(data):

    return json.loads(data)


def dump_json(data):

    return json.dumps(data, indent=2, ensure_ascii=False)


def wget_obj(url):

    if os.path.exists(url):
        _, ext = os.path.splitext(url)
        if ext in ['.json']:
            return json.load(open(url))
        elif ext in ['.yaml', '.yml']:
            return yaml.load(open(url))
        else:
            raise Exception('cannot detect resource type')
    else:
        return requests.get(url, timeout=3).json()


def load_conf(fname):

    if os.path.exists(fname):
        _, ext = os.path.splitext(fname)
        if ext in ['.json']:
            return json.load(open(fname))
        elif ext in ['.yaml', '.yml']:
            return yaml.load(open(fname))
        else:
            raise Exception('cannot detect resource type')
    else:
        raise Exception('config file not found')


def update_request(cfg):

    for dp in cfg.get('dsp').get('s'):
        nf = dp.get('notice_file')
        rf = dp.get('res_file')
        if isinstance(nf, str) and os.path.exists(nf):
            try:
                dp['notice_file'] = load_conf(nf)
            except Exception:
                logging.warn('notice_file format error')
                with open(nf) as f:
                    dp['notice_file'] = f.read()
        if isinstance(rf, str) and os.path.exists(rf):
            try:
                dp['res_file'] = load_conf(rf)
            except Exception:
                logging.warn('res_file format error')
                with open(rf) as f:
                    dp['res_file'] = f.read()
    return cfg


def load_file(fname):
    with open(fname) as f:
        return json.loads(f.read())


def compare_dictionaries(x, y):

    '''x contains y'''

    if type(x) != type(y):
        return False

    if isinstance(y, list):
        if len(y) > len(x):
            return False
        for i in zip(x, y):
            if not compare_dictionaries(*i):
                return False
        else:
            return True

    if isinstance(y, dict):
        for y_k, y_v in y.items():
            if y_k not in x:
                return False
            if not compare_dictionaries(x[y_k], y_v):
                return False
        else:
            return True

    return x == y


def timeit(func):
    @functools.wraps(func)
    def wrapper():
        start = time.clock()
        func()
        end = time.clock()
        return (end - start)
    return wrapper
